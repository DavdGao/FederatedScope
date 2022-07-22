from mimetypes import init
from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.data_pb2 import Schema, DataType
from federatedscope.db.model.sqlquery_pb2 import Operator
from google.protobuf import text_format
from federatedscope.db.algorithm.hdtree import LDPHDTree

import numpy as np


class MdaProcessor(BasicSQLProcessor):
    def __init__(self, epsilon, fanout):
        super(MdaProcessor, self).__init__()
        self.eps = epsilon
        self.fanout = fanout

    def get_simple_agg(self, query):
        """
        get simple aggregate exps in the query plan.
        a simple aggregate means the expression has only one aggregate function,
        and the aggregate function directly takes an attribtue as input 

        Returns:
            list of (attribute name, aggregate function)
        """
        agg_exps = query.querypb.exp_agg
        aggregates = []
        for exp in agg_exps:
            attr = exp.children[0].s
            aggregates.append((attr, exp.operator))
        return aggregates

    def get_range_predicate(self, query):
        """
        get range filters in predicate
        
        Returns:
            list of (attribute name, (min_value, max_value))
        """
        where_exps = query.querypb.exp_where
        filters = {}
        for exp in where_exps:
            children = exp.children
            if children[0].operator == Operator.REF and children[
                    1].operator == Operator.LIT:
                attr = children[0].s
                lit_type = children[1].type
                if lit_type == DataType.INT:
                    value = children[1].i
                elif lit_type == DataType.FLOAT:
                    value = children[1].f
                else:
                    value = children[1].s
            else:
                raise ValueError("Only supports column compare with value")
            if exp.operator == Operator.GE:
                if attr not in filters:
                    filters[attr] = {}
                    filters[attr]['min'] = value
                elif 'min' not in filters[attr]:
                    filters[attr]['min'] = value
                else:
                    raise ValueError("Unsupported overlap range")
            elif exp.operator == Operator.LE:
                if attr not in filters:
                    filters[attr] = {}
                    filters[attr]['max'] = value
                elif 'max' not in filters[attr]:
                    filters[attr]['max'] = value
                else:
                    raise ValueError("Unsupported overlap range")
            elif exp.operator == Operator.EQ:
                if attr in filters:
                    raise ValueError("Unsupported overlap range")
                else:
                    filters[attr] = {}
                    filters[attr]['min'] = value
                    filters[attr]['max'] = value
            else:
                raise ValueError("Only supports =, <=, >= in where clause")
        return filters

    def check(self, query):
        if len(self.get_simple_agg(query)) != 1:
            raise ValueError("only supports one aggregate function")
        self.get_range_predicate(query)

    def prepare(self, table):
        encoded_schema = text_format.Parse(table.schema.schemapb.attributes[-1].name, Schema())
        self.hd_tree = LDPHDTree(encoded_schema.attributes, self.eps, self.fanout)

    def query(self, query, table):
        """
        query on local tables
        Args:
            query (Query): query plan
            table (Table): the table
        """

        filters = self.get_range_predicate(query)

        # Deal with aggregation
        agg_attr, agg_type = self.get_simple_agg(query)[0]
        agg_buffer = np.zeros(3)

        # Obtain the query layers in the hdtree
        query_hd_layers, query_hd_intervals = self.hd_tree.get_query_layers(filters)
        # decode each row using hdtree
        for i, row in table.data.iterrows():
            agg_value = row[agg_attr]
            self.hd_tree.add(agg_buffer, row[-1], agg_value, query_hd_layers,
                       query_hd_intervals)

        # Obtain the aggregation result
        if agg_type == Operator.COUNT:
            return agg_buffer[0]
        elif agg_type == Operator.SUM:
            return agg_buffer[1]
        elif agg_type == Operator.AVG:
            return float(agg_buffer[1]) / agg_buffer[0]
        else:
            raise ValueError("unsupported aggregate function")
