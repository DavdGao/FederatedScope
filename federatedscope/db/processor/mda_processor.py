from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.data_pb2 import Schema
from federatedscope.db.model.sqlquery_pb2 import Operator
from google.protobuf import text_format
from federatedscope.db.algorithm.hdtree import LDPHDTree

import numpy as np


class MdaProcessor(BasicSQLProcessor):
    def __init__(self, eps, fanout):
        super(MdaProcessor, self).__init__()

        self.eps = eps
        self.fanout = fanout

    def check(self):
        # TODO: @xuchen, check if the query is a mda query
        pass

    # TODO: we should replace table by accessor
    def execute(self, query, table):
        """
        query on local tables
        Args:
            query (Query): query plan
            table (Table): the table
        """
        encoded_schema = text_format.Parse(
            table.schema.schemapb.attributes[-1].name, Schema())

        # TODO: @xuchen, maybe build in the __init__ function
        # Build the LDPHDTree for each query
        hdtree = LDPHDTree(encoded_schema.attributes, self.eps, self.fanout)

        filters = query.get_range_predicate()

        # Deal with aggregation
        agg_attr, agg_type = query.get_simple_agg()[0]
        agg_buffer = np.zeros(3)

        # Obtain the query layers in the hdtree
        query_hd_layers, query_hd_intervals = hdtree.get_query_layers(filters)
        # TODO: @xuchen, add some comments here
        for i, row in table.data.iterrows():
            agg_value = row[agg_attr]
            hdtree.add(agg_buffer, row[-1], agg_value, query_hd_layers,
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
