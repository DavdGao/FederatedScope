import federatedscope.db.accessor.data as data
import federatedscope.db.model.data_pb2 as datapb
from federatedscope.db.algorithm.ldp import LDPOLH

import itertools
import random


class RangeTree(object):
    def __init__(self):
        self.children = []
        self.range = None
        self.layer = None
        self.height = None
        random.seed()

    @staticmethod
    def factory(min, max, delta, fanout):
        root = RangeTree().construct(min, max, 0, delta, fanout)
        return root

    # todo: check float value
    def construct(self, min, max, layer, delta, fanout):
        self.range = (min, max)
        self.layer = layer
        self.height = 1
        if max - min + 1 > delta:
            step_size = int((max - min + 1) / fanout)
            if step_size == 0:
                step_size = 1
            cur_min, cur_max = min, min + step_size - 1
            while cur_min <= max:
                if cur_max >= max:
                    cur_max = max
                child = RangeTree().construct(cur_min, cur_max, layer + 1,
                                              delta, fanout)
                if self.height < child.height + 1:
                    self.height = child.height + 1
                self.children.append(child)
                cur_min, cur_max = cur_min + step_size, cur_max + step_size
        return self

    def decompose_interval(self, min, max):
        if min <= self.range[0] and self.range[1] <= max:
            return [(self.layer, self.range)]
        ret = []
        for child in self.children:
            if min <= child.range[0] <= max or min <= child.range[1] <= max:
                ret += child.decompose_interval(min, max)
        return ret

    def get_ranges(self, value):
        ret = [None] * self.height
        node = self
        while node != None:
            ret[node.layer] = node.range
            next_node = None
            for child in node.children:
                if child.range[0] <= value <= child.range[1]:
                    next_node = child
                    break
            node = next_node
        return ret


class LDPHDTree(object):
    def __init__(self, sensitive_attrs, eps, fanout):
        """
        build range trees based on local table
        Args:
            table (data.Table): table python object
            eps (float): the epsilon parameter
            fanout (int): fanout of hd tree
        """
        self.sensitive_attributes = sensitive_attrs
        self.fanout = fanout
        self.eps = eps
        self.fo = LDPOLH(eps)
        self.build_range_trees()

    def build_range_trees(self):
        self.trees = {}
        self.tree_heights = {}
        for attr in self.sensitive_attributes:
            if attr.type == datapb.DataType.INT:
                tree = RangeTree.factory(attr.min_value.i, attr.max_value.i,
                                         attr.delta.i, self.fanout)
                self.trees[attr.name] = tree
                self.tree_heights[attr.name] = tree.height
            elif attr.type == datapb.DataType.FLOAT:
                tree = RangeTree.factory(attr.min_value.f, attr.max_value.f,
                                         attr.delta.f, self.fanout)
                self.trees[attr.name] = tree
                self.tree_heights[attr.name] = tree.height
            else:
                self.trees[attr.name] = None
                self.tree_heights[attr.name] = 2
        layers = [
            range(self.tree_heights[attr.name])
            for attr in self.sensitive_attributes
        ]
        self.hdnode_layers = [
            report_layer for report_layer in itertools.product(*layers)
        ]

    def decode(self, report, hd_layers, hd_intervals):
        (report_layers, report_value) = eval(report)
        result = 0
        for i, layer in enumerate(hd_layers):
            if report_layers == layer:
                result += self.fo.decodes(report_value, hd_intervals[i]) * len(
                    self.hdnode_layers)
        return result

    def encode_row(self, row):
        report_layer = random.choice(self.hdnode_layers)
        values = []
        for i, layer in enumerate(report_layer):
            attr = self.sensitive_attributes[i]
            tree = self.trees[self.sensitive_attributes[i].name]
            if attr.type == datapb.DataType.INT or attr.type == datapb.DataType.FLOAT:
                values.append(tree.get_ranges(row[i])[layer])
            else:
                if layer == 0:
                    values.append(None)
                else:
                    values.append(row[i])
        perturbed_value = self.fo.encodes(str(values))
        return str((report_layer, perturbed_value))

    def encode_table(self, table):
        # generate report for each row
        sensitive_attr_names = map(lambda attr: attr.name,
                                   self.sensitive_attributes)
        encoded_schema = datapb.Schema()
        encoded_schema.attributes.extend(self.sensitive_attributes)
        encoded_reports = []
        for i, row in table.project(sensitive_attr_names).iterrows():
            encoded_reports.append(self.encode_row(row))

        # get unsensitive part of table
        unsensitive_attrs = table.schema.unsensitive_attrs()
        encoded_table = datapb.Table()
        encoded_table.name = table.name
        encoded_table.config = str({
            'eps': self.eps,
            'fanout': self.fanout
        })
        encoded_table.data.schema.attributes.extend(unsensitive_attrs)
        report_attr = encoded_table.data.schema.attributes.add()

        report_attr.name = str(encoded_schema)
        report_attr.type = datapb.DataType.STRING
        report_attr.sensitive = True
        unsensitive_attr_names = map(lambda attr: attr.name, unsensitive_attrs)
        for i, row in table.project(unsensitive_attr_names).iterrows():
            rowpb = encoded_table.data.rows.rows.add()
            j = 0
            for cell in row:
                cellpb = rowpb.cells.add()
                if unsensitive_attrs[j].type == datapb.DataType.INT:
                    cellpb.i = cell
                elif unsensitive_attrs[j].type == datapb.DataType.FLOAT:
                    cellpb.f = cell
                else:
                    cellpb.s = cell
                j += 1
            # append report to each row
            reportpb = rowpb.cells.add()
            reportpb.s = encoded_reports[i]
        return encoded_table

    def get_query_layers(self, filters):
        attribute_constraints = []
        for i, attr in enumerate(self.sensitive_attributes):
            if attr.type == datapb.DataType.INT or attr.type == datapb.DataType.FLOAT:
                interval = None
                if attr.type == datapb.DataType.INT:
                    interval = [attr.min_value.i, attr.max_value.i]
                else:
                    interval = [attr.min_value.f, attr.max_value.f]
                if attr.name in filters:
                    if 'min' in filters[attr.name]:
                        interval[0] = filters[attr.name]['min']
                    if 'max' in filters[attr.name]:
                        interval[1] = filters[attr.name]['max']
                attribute_constraints.append(
                    self.trees[attr.name].decompose_interval(
                        interval[0], interval[1]))
            else:
                if attr.name in filters:
                    str_value = (1, filters[attr.name]['min'])
                else:
                    str_value = (0, None)
                attribute_constraints.append([str_value])
        query_hd = [hd for hd in itertools.product(*attribute_constraints)]
        query_hd_layers = []
        query_hd_intervals = []
        for hd in query_hd:
            hd_layer = []
            hd_interval = []
            for layer, value in hd:
                hd_layer.append(layer)
                hd_interval.append(value)
            query_hd_layers.append(tuple(hd_layer))
            query_hd_intervals.append(hd_interval)
        return (query_hd_layers, query_hd_intervals)

    def add(self, buffer, report, agg_value, query_hd_layers,
            query_hd_intervals):
        result = self.decode(report, query_hd_layers, query_hd_intervals)
        buffer[0] += result
        buffer[1] += result * agg_value
        buffer[2] += agg_value
