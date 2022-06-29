import federatedscope.db.data.data as data
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
            step_size = ((max - min + 1) / fanout)
            if step_size == 0:
                step_size = 1
            cur_min, cur_max = min, min + step_size - 1
            while cur_min <= max:
                if cur_max >= max:
                    cur_max = max
                child = RangeTree().construct(cur_min, cur_max, layer + 1, delta, fanout)
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
    def __init__(self, table, eps, fanout):
        """
        build range trees based on local table
        Args:
            table (data.Table): table python object
            eps (float): the epsilon parameter
            fanout (int): fanout of hd tree
        """
        self.table = table
        self.fanout = fanout
        self.fo = LDPOLH(eps)
        self.build_range_trees()

    def build_range_trees(self):
        self.sensitive_attributes = self.table.schema.sensitive_attrs()
        self.trees = {}
        self.tree_heights = {}
        for attr in self.sensitive_attributes:
            if attr.type == datapb.DataType.INT:
                tree = RangeTree.factory(attr.min_value.i, attr.max_value.i, attr.delta.i, self.fanout)
                self.trees[attr.name] = tree
                self.tree_heights[attr.name] = tree.height
            elif attr.type == datapb.DataType.FLOAT:
                tree = RangeTree.factory(attr.min_value.f, attr.max_value.f, attr.delta.f, self.fanout)
                self.trees[attr.name] = tree
                self.tree_heights[attr.name] = tree.height
            else:
                self.tree[attr.name] = None
                self.tree_heights[attr.name] = 2
        layers = [range(self.tree_heights[attr.name]) for attr in self.sensitive_attributes]
        self.hdnode_layers = [report_layer for report_layer in itertools.product(*layers)]


    def encode_row(self, row):
        print(row)
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

    def encode_table(self):
        # generate report for each row
        sensitive_attr_names = map(lambda attr : attr.name, self.sensitive_attributes)
        encoded_reports = []
        for i, row in self.table.project(sensitive_attr_names).iterrows():
            encoded_reports.append(self.encode_row(row))

        # get unsensitive part of table
        unsensitive_attrs = self.table.schema.unsensitive_attrs()
        encoded_table = datapb.Table()
        encoded_table.name = self.table.name
        encoded_table.data.schema.attributes.extend(unsensitive_attrs)
        report_attr = encoded_table.data.schema.attributes.add()
        report_attr.name = "$report$"
        report_attr.type = datapb.DataType.STRING
        report_attr.sensitive = True
        unsensitive_attr_names = map(lambda attr : attr.name, unsensitive_attrs)
        for i, row in self.table.project(unsensitive_attr_names).iterrows():
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