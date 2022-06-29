from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.algorithm.ldp import LDPOLH
from federatedscope.db.algorithm.hdtree import LDPHDTree
import federatedscope.db.model.sqlquery_pb2 as sqlpb
import federatedscope.db.data.data as data
import federatedscope.db.model.data_pb2 as datapb
import federatedscope.db.data.data_accessor as data_accessor

import pandas as pd
import numpy as np
import os


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

    def encode_table(self, table_name: str, eps: float, fanout: int):
        if not self.has_table(table_name):
            raise ValueError("table " + table_name + " not exists")
        table = self.get_table(table_name)
        hdtree = LDPHDTree(table, eps, fanout)
        encoded_table = hdtree.encode_table()
        return encoded_table


    def query(self, query):
        """
        query on local tables
        Args:
            query (sqlpb.BasicSchedule): protocol buffer of query plan
        """
        pass
