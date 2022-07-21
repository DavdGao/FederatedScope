from mimetypes import init
from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.data_pb2 import Schema
from federatedscope.db.model.sqlquery_pb2 import Operator
from google.protobuf import text_format
from federatedscope.db.algorithm.hdtree import LDPHDTree

import numpy as np


class MdaProcessor(BasicSQLProcessor):
    def __init__(self, epsilon, fanout):
        super(MdaProcessor, self).__init__()
        self.eps = epsilon
        self.fanout = fanout

    def check(self):
        # TODO: @xuchen, check if the query is a mda query
        pass

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

        filters = query.get_range_predicate()

        # Deal with aggregation
        agg_attr, agg_type = query.get_simple_agg()[0]
        agg_buffer = np.zeros(3)

        # Obtain the query layers in the hdtree
        query_hd_layers, query_hd_intervals = self.hd_tree.get_query_layers(filters)
        # TODO: @xuchen, add some comments here
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
