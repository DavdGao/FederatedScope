from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.algorithm.ldp import LDPOLH
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

    def encode_table(self, table_name: str, eps: float):
        if not self.has_table(table_name):
            raise ValueError("table " + table_name + " not exists")
        table = self.get_table(table_name)
        olh = LDPOLH(eps)
        encoded_table = datapb.Table()
        encoded_table.name = table_name
        table = self.get_table(table_name)
        for attr in table.schema.schemapb.attributes:
            encoded_attr = encoded_table.data.schema.attributes.add()
            encoded_attr.CopyFrom(attr)
            if attr.sensitive:
                # encode into int64 olh report
                encoded_attr.type = datapb.DataType.INT
        for rowid, data in table.data.iterrows():
            encoded_row = encoded_table.data.rows.rows.add()
            i = 0
            for attr in encoded_table.data.schema.attributes:
                encoded_cell = encoded_row.cells.add()
                if attr.type == datapb.DataType.INT:
                    encoded_cell.i = data[i]
                elif attr.type == datapb.DataType.FLOAT:
                    encoded_cell.f = data[i]
                else:
                    encoded_cell.s = data[i]
                # for sensitive value, put OLH report in int field
                if attr.sensitive:
                    encoded_cell.i = olh.encodes(data[i])
                i += 1
        return encoded_table


    def query(self, query):
        """
        query on local tables
        Args:
            query (sqlpb.BasicSchedule): protocol buffer of query plan
        """
        pass
