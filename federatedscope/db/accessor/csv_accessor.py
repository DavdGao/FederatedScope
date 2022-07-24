import pandas as pd
import numpy as np

import federatedscope.db.model.data_pb2 as datapb
import federatedscope.db.accessor.data as data

from federatedscope.db.accessor.basic_accessor import BasicAccessor


class CsvAccessor(BasicAccessor):
    """Create a csv accessor, where the schema should be specified by input parameter schema

    """
    def __init__(self, root, schema):
        super(CsvAccessor, self).__init__(root)

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
        schema = self.parse_schema(schema)
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

    def parse_schema(self, schema):
        """
        parse a schema string
        Args:
            schema (list): schema of the csv file, contains a list of attribute descriptions, see parse_attribute for details

        Returns:
            Wrapper of protocol buffer Schema
        """
        schemapb = datapb.Schema()
        attrpbs = []
        for attr in schema:
            if 'name' not in attr:
                raise ValueError("No name in attribute definition")
            if 'type' not in attr:
                raise ValueError("No type in attribute definition")
            attrpbs.append(self.parse_attribute(attr))
        schemapb.attributes.extend(attrpbs)
        return data.Schema(schemapb)

    def parse_attribute(self, attr):
        """
        parse attribute description into protocol buffer Attribute
        Args:
            attr: a dictionary describing attribute information, format:
            {
                'name': attribute name,
                'type': accessor type(int|float|string),
                'sensitve': whether the attribute is sensitive(optional, default false),
                'min': int value(optional),
                'max': max value(optional),
                'delta': value interval(optional)
            }

        Returns:
            protocol buffer Attribute
        """
        # TODO: @xuchen, It seems like the attributes of pb class are related to the keys in the dict, can we build a smart translator？
        attrpb = datapb.Attribute()
        attrpb.name = attr['name']
        if attr['type'].lower() == 'int':
            attrpb.type = datapb.DataType.INT
        elif attr['type'].lower() == 'float':
            attrpb.type = datapb.DataType.FLOAT
        else:
            attrpb.type = datapb.DataType.STRING
        if 'sensitive' in attr:
            attrpb.sensitive = bool(attr['sensitive'])
        if 'primary' in attr:
            attrpb.primary = bool(attr['primary'])
        # set has_range when schema gives min max and delta
        if 'min' in attr and 'max' in attr and 'delta' in attr:
            if attrpb.type == datapb.DataType.INT:
                attrpb.min_value.i = int(attr['min'])
                attrpb.max_value.i = int(attr['max'])
                attrpb.delta.i = int(attr['delta'])
                attrpb.has_range = True
            elif attrpb.type == datapb.DataType.FLOAT:
                attrpb.min_value.f = float(attr['min'])
                attrpb.max_value.f = float(attr['max'])
                attrpb.delta.f = float(attr['delta'])
                attrpb.has_range = True
            else:
                attrpb.has_range = False
        else:
            attrpb.has_range = False
        return attrpb

    def get_schema(self, table_name):
        # TODO: consider multiple tables in the future
        if table_name == self.table.name:
            return self.table.schema
        else:
            raise ValueError(f'Table {table_name} not found.')

    def get_table(self, table_name=None):
        # TODO: consider multiple tables in the future
        return self.table
