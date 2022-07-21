import federatedscope.db.accessor.csv_accessor as data_accessor


class BasicSQLProcessor(object):
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

    # def execute(self, query, **kwargs):
    #     pass

    def check(self, query):
        return True
