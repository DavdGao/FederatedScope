from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.sqlschedule import Query
from federatedscope.db.model.sqlquery_pb2 import Operator
from federatedscope.db.data.data import Table
from federatedscope.db.model.data_pb2 import Schema
from federatedscope.db.algorithm.hdtree import LDPHDTree

import numpy as np
from google.protobuf import text_format

class ExternalSQLProcessor(BasicSQLProcessor):
    def mda_query(self, query, table, eps: float, fanout: int):
        """
        process mda query on the specific table

        Args:
            query (Query): the mda query plan
            table (Table): the target table
            eps (float): ldp parameter
            fanout (int): hdtree parameter
        """
        encoded_schema = text_format.Parse(table.schema.schemapb.attributes[-1].name, Schema())
        hdtree = LDPHDTree(encoded_schema.attributes, eps, fanout)
        filters = query.get_range_predicate()
        aggs = query.get_simple_agg()[0]
        agg_attr = aggs[0]
        agg_type = aggs[1]
        agg_buffer = np.zeros(3)
        (query_hd_layers, query_hd_intervals) = hdtree.get_query_layers(filters)
        for i, row in table.data.iterrows():
            agg_value = row[agg_attr]
            hdtree.add(agg_buffer, row[-1], agg_value, query_hd_layers, query_hd_intervals)
        if agg_type == Operator.CNT:
            return agg_buffer[0]
        elif agg_type == Operator.SUM:
            return agg_buffer[1]
        elif agg_type == Operator.AVG:
            return float(agg_buffer[1]) / agg_buffer[0]
        else:
            raise ValueError("unsupported aggregate function")
