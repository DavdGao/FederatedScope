import pandas as pd
import numpy as np

import federatedscope.db.model.data_pb2 as datapb
import federatedscope.db.accessor.data as data

from federatedscope.db.accessor.basic_accessor import BasicAccessor


class CsvAccessor(BasicAccessor):
    """Create a csv accessor, where the schema should be specified by input parameter schema

    """
    def __init__(self, root, schema):
        super(CsvAccessor, self).__init__()

        self.root = root

        # TODO: consider multiple tables in the future
        # Load schema from string
        self.table = None

        # Connect to the DBMS
        self.connect(schema)

    def connect(self, schema):
        """Load the csv table

        Args:
            schema (list)

        Returns:

        """
        # TODO: optimize schema config format
        schema = data.parse_schema(schema)
        # Load csv file
        df = pd.read_csv(self.root,
                         names=schema.names(),
                         header=0,
                         skipinitialspace=True)
        # Trans accessor type
        for attr in schema.attrs():
            if attr.type == datapb.DataType.INT:
                df[attr.name] = df[attr.name].values.astype(np.int64)
            elif attr.type == datapb.DataType.FLOAT:
                df[attr.name] = df[attr.name].values.astype(np.float64)
            else:
                df[attr.name] = [
                    t.strip() for t in df[attr.name].values.astype(np.str)
                ]
        # Create table
        table_name = self.root.split('/')[-1].replace('.csv', '')
        self.table = data.Table(table_name, schema, df)

    def get_schema(self, table_name):
        # TODO: consider multiple tables in the future
        if table_name == self.table.name:
            return self.table.schema
        else:
            raise ValueError(f'Table {table_name} not found.')

    def get_table(self, table_name=None):
        # TODO: consider multiple tables in the future
        return self.table
