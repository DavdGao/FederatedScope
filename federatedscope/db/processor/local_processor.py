from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.sqlquery import SQLQuery, Filter, Aggregate
from federatedscope.db.data.schema import Attribute, Schema
from federatedscope.db.data.data import Data

import pandas as pd
import os


class LocalSQLProcessor(BasicSQLProcessor):
    # read all csv files in datadir, and use file name as table name
    def __init__(self, datadir: str):
        self.tables = {}
        self.schemas = {}
        datafiles = os.listdir(datadir)
        for file in datafiles:
            if file.endswith('.csv'):
                table_name = os.path.splitext(file)[0]
                df = pd.read_csv(os.path.join(datadir, file))
                self.tables[table_name] = df
                print("load table " + file + "with columns:")
                print(df.columns)
                self.schemas[table_name] = self.__convert_schema(
                    df, df.columns)

    def get_table(self, table_name: str):
        return self.tables[table_name]

    def get_schema(self, table_name: str):
        return self.schemas[table_name]

    def __convert_schema(self, df, attr_names) -> Schema:
        attrs = []
        if isinstance(df, pd.DataFrame):
            for attr in zip(attr_names, df.dtypes):
                attrs.append(Attribute(attr[0], attr[1]))
        else:
            attrs.append(Attribute(attr_names[0], type(df)))
        return Schema(attrs)

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

