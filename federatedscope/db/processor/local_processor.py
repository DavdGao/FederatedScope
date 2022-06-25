from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.sqlschedule_pb2 import DataType
from federatedscope.db.model.backup import SQLQuery, Filter, Aggregate
from federatedscope.db.data.schema import Attribute, Schema
from federatedscope.db.data.data import Data


import pandas as pd
import numpy as np
import os


class LocalSQLProcessor(BasicSQLProcessor):
    def __init__(self):
        self.tables = {}
        self.schemas = {}

    def load_table(self, table_name: str, schema_str: str, table_path: str):
        schema = Schema(schema_str)
        df = pd.read_csv(table_path, header=0,
                         names=schema.attr_names(), skipinitialspace=True)
        print("load table " + table_name + " from " + table_path)
        for attr in schema.attrss():
            if attr.type == DataType.INT:
                df[attr.name] = df[attr.name].values.astype(np.int32)
            else:
                df[attr.name] = [t.strip()
                                 for t in df[attr.name].values.astype(np.str)]
        self.tables[table_name] = df
        self.schemas[table_name] = schema

    def get_table(self, table_name: str):
        return self.tables[table_name]

    def get_schema(self, table_name: str):
        return self.schemas[table_name]

    def __convert(self, qid, df, attrs) -> Data:
        schema = self.__convert_schema(df, attrs)
        if isinstance(df, pd.DataFrame):
            return Data(qid, schema, df.values.tolist())
        else:
            return Data(qid, schema, [[df]])

    def query(self, query: SQLQuery):
        tb = self.get_table(query.table_name)
        if query.filters != None:
            for filt in query.filters:
                tb = tb[(tb[filt.attr] >= filt.left) &
                        (tb[filt.attr] <= filt.right)]
        if query.attrs != None and len(query.attrs) > 0:
            return self.__convert(query.qid, tb[query.attrs], query.attrs)
        elif query.aggregate != None:
            agg_type = query.aggregate.func_type
            agg_attr = query.aggregate.attr
            if agg_type == 'COUNT':
                return self.__convert(query.qid, tb[agg_attr].count(), ["COUNT(%s)" % agg_attr])
            elif agg_type == "SUM":
                return self.__convert(query.qid, tb[agg_attr].sum(), ["SUM(%s)" % agg_attr])
            else:
                raise NotImplementedError("Unsupported aggregate function")
        else:
            raise ValueError("No output in query")
