from federatedscope.db.accessor.basic_accessor import BasicAccessor
import federatedscope.db.accessor.data as data

from sqlalchemy import create_engine
import pandas as pd

class MySqlAccessor(BasicAccessor):
    def __init__(self, user, passwd, host, port, database, schemas):
        """
        connect to mysql

        Args:
            user (string): user of mysql
            passwd (string): passwd of the user
            host (string): hostname of mysql
            port (int): port of mysql
            database (string): database to connect
            schemas (dic): { <table_name>: <table_schema>, ...}
                            e.g.
                            {
                                'user': [
                                    {'name':'id','type':'int','primary':True},
                                    {'name':'age','type':'int','min':17,'max':81,'delta':1}
                                ]
                            }
        """
        super(MySqlAccessor, self).__init__()
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, passwd, host, port, database))
        self.tables = {}
        self.schemas = {}
        self.connect(schemas)

    # todo: support multiple schemas
    def connect(self, schemas):
        for name, schema in schemas.items():
            self.schemas[name] = data.parse_schema(schema)

    def get_schema(self, table_name):
        return self.schemas[table_name]

    def get_table(self, table_name):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.engine)
        return data.Table(table_name, self.schemas[table_name], df)

    def close(self):
        self.cursor.close()
