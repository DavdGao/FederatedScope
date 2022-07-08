from federatedscope.db.processor.basic_processor import BasicSQLProcessor
import federatedscope.db.data.data as data
import federatedscope.db.model.sqlquery_pb2 as querypb
import federatedscope.db.data.csv_accessor as data_accessor
from federatedscope.db.algorithm.hdtree import LDPHDTree

import numpy as np


class LocalSQLProcessor(BasicSQLProcessor):
    def __init__(self):
        self.tables = {}
        self.schemas = {}

    def load_table(self, table_path: str, schema_str: str):
        table = data_accessor.load_csv(table_path, schema_str)
        self.tables[table.name] = table

    def has_table(self, table_name: str):
        return table_name in self.tables

    def get_table(self, table_name: str):
        return self.tables[table_name]

    def get_schema(self, table_name: str):
        return self.schemas[table_name]

    def encode_table(self, table, eps: float, fanout: int):
        """
        encode table with hd tree

        Args:
            table (data.Table): table to be encoded
            eps (float): ldp epsilon parameter
            fanout (int): hdtree parameter

        Returns:
            (hdtree, encoded table)
        """
        hdtree = LDPHDTree(table.schema.sensitive_attrs(), eps, fanout)
        encoded_table = hdtree.encode_table(table)
        return (hdtree, encoded_table)

    def mda_query(self, query, eps: float, fanout: int):
        """
        query on local tables
        Args:
            query (Query): query plan
            eps (float): ldp epsilon parameter
            fanout (int): hdtree parameter
        """
        table_name = query.target_table_name()
        (hdtree, encoded_table) = self.encode_table(table_name, eps, fanout)
        table = data.Table.from_pb(encoded_table)
        filters = query.get_range_predicate()
        aggs = query.get_simple_agg()[0]
        agg_attr = aggs[0]
        agg_type = aggs[1]
        agg_values = table.project([agg_attr])
        agg_buffer = np.zeros(3)
        (query_hd_layers, query_hd_intervals) = hdtree.get_query_layers(filters)
        for i, row in table.data.iterrows():
            agg_value = row[agg_attr]
            hdtree.add(agg_buffer, row[-1], agg_value, query_hd_layers, query_hd_intervals)
        if agg_type == querypb.Operator.CNT:
            return agg_buffer[0]
        elif agg_type == querypb.Operator.SUM:
            return agg_buffer[1]
        elif agg_type == querypb.Operator.AVG:
            return float(agg_buffer[1]) / agg_buffer[0]
        else:
            raise ValueError("unsupported aggregate function")
