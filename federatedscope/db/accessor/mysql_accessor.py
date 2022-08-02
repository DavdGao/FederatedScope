from federatedscope.db.accessor.basic_accessor import BasicAccessor

import pymysql

class MySqlAccessor(BasicAccessor):
    def __init__(self, user, passwd, database):
        super(MySqlAccessor, self).__init__()
        self.database = database
        self.cursor = self.connect(user, passwd, database)

    def connect(self, user, passwd, database):
        # For now, we only support local dbms
        db = pymysql.connect(host='localhost',
                             user=user,
                             password=passwd,
                             database=database)

        cursor = db.cursor()
        return cursor

    def get_schema(self, table_name):
        self.cursor.execute(f"describe {self.database}.{table_name};")
        # Parse into pb
        print(self.cursor.fetchall())


    def get_table(self, table_name):
        self.cursor.execute("SELECT * FROM {table_name}")
        # Actually we can read the data one by one
        return self.cursor.fetchall()


    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    acc = MySqlAccessor('root', '123456', 'mysql')
    acc.get_schema('user')