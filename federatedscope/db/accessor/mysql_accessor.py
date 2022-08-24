from federatedscope.db.accessor.basic_accessor import BasicAccessor
import federatedscope.db.accessor.data as data

from sqlalchemy import create_engine
import pandas as pd

class MySqlAccessor(BasicAccessor):
    def __init__(self, root, schema):
        """
        connect to mysql

        Args:
            root(string): "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}"
            schema (list): [ {schema of a table}, ... ]
                            e.g.
                            [{
                                'name': 'user',
                                'schema': [
                                    {'name':'id','type':'int','primary':True},
                                    {'name':'age','type':'int','min':17,'max':81,'delta':1}
                                ]
                            },...]
        """
        super(MySqlAccessor, self).__init__()
        self.engine = create_engine(root)
        self.tables = {}
        self.schemas = {}
        self.default_table = ""
        self.connect(schema)

    # todo: support multiple schemas
    def connect(self, schema):
        for table in schema:
            if self.default_table == "":
                self.default_table = table['name']
            self.schemas[table['name']] = data.parse_schema(table['schema'])

    def get_schema(self, table_name):
        return self.schemas[table_name]
    
    def get_table(self):
        df = pd.read_sql_query(f"SELECT * FROM {self.default_table}", self.engine)
        return data.Table(self.default_table, self.schemas[self.default_table], df)

    def get_table(self, table_name):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.engine)
        return data.Table(table_name, self.schemas[table_name], df)
