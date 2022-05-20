from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.sqlquery import SQLQuery, Filter, Aggregate

import pandas as pd
import os

class LocalSQLProcessor(BasicSQLProcessor):
    # read all csv files in datadir, and use file name as table name
    def __init__(self, datadir):
        self.tables = {}
        datafiles = os.listdir(datadir)
        for file in datafiles:
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(datadir, file))
                self.tables[os.path.splitext(file)[0]] = df
                print("load table " + file + "with columns:")
                print(df.columns)

    def get_table(self, table_name):
        return self.tables[table_name]

    def query(self, query):
        tb = self.get_table(query.table_name)
        if query.filters != None:
            for filt in query.filters:
                tb = tb[(tb[filt.attr] > filt.left) & (tb[filt.attr] < filt.right)]
        if query.attrs != None and len(query.attrs) > 0:
            tb = tb[query.attrs]
        elif query.aggregate != None:
            agg_type = query.aggregate.func_type
            agg_attr = query.aggregate.attr
            if agg_type == 'COUNT':
                tb = tb[agg_attr].count()
            elif agg_type == "SUM":
                tb = tb[agg_attr].sum()
            else:
                raise NotImplementedError("Unsupported aggregate function")
        else:
            raise ValueError("No output in query")
        return tb
