from federatedscope.db.processor.basic_processor import BasicSQLProcessor
import federatedscope.db.model.sqlquery_pb2 as sqlpb
import federatedscope.db.data.data as data
import federatedscope.db.model.data_pb2 as datapb

import pandas as pd
import numpy as np
import os


class LocalSQLProcessor(BasicSQLProcessor):
    def __init__(self):
        self.tables = {}
        self.schemas = {}

    def load_table(self, table_path: str, schema_str: str):
        table = data.load_csv(table_path, schema_str)
        self.tables[table.name] = table
        self.schemas[table_name] = table.schema

    def get_table(self, table_name: str):
        return self.tables[table_name]

    def get_schema(self, table_name: str):
        return self.schemas[table_name]

    def query(self, query):
        """
        query on local tables
        Args:
            query (sqlpb.BasicSchedule): protocol buffer of query plan
        """
       pass
