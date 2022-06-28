import pandas as pd
import numpy as np

import federatedscope.db.model.data_pb2 as datapb
import federatedscope.db.data.data as data

def parse_attribute(attr):
    """
    parse attribute description into protocol buffer Attribute
    Args:
        attr: a dictionary describing attribute information, format:
        {
            'name': attribute name,
            'type': data type(int|float|string),
            'sensitve': whether the attribute is sensitive(optional, default false),
            'min': int value(optional),
            'max': max value(optional),
            'delta': value interval(optional)
        }

    Returns:
        protocol buffer Attribute
    """
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


def parse_schema(schema_str):
    """
    parse a schema string 
    Args:
        schema_str (string): schema of the csv file in string, contains a list of attribute descriptions, see parse_attribute for details

    Returns:
        Wrapper of protocol buffer Schema
    """
    schema = datapb.Schema()
    attrs = eval(schema_str.strip())
    attrpbs = []
    for attr in attrs:
        if 'name' not in attr:
            raise ValueError("No name in attribute definition")
        if 'type' not in attr:
            raise ValueError("No type in attribute definition")
        attrpbs.append(parse_attribute(attr))
    schema.attributes.extend(attrpbs)
    return data.Schema(schema)




def load_csv(path, schema_str):
    """
    load a csv file 
    Args:
        path (string): the path to the csv file (use file name as table name)
        schema_str (string): see parse_schema for details
    Returns:
        Table: Wrapper of protocol buffer Table
    """
    # todo: optimize schema config format
    schema = parse_schema(schema_str)
    df = pd.read_csv(
        path,
        names=schema.names(),
        header=0,
        skipinitialspace=True
    )
    for attr in schema.attrs():
        if attr.type == datapb.DataType.INT:
            df[attr.name] = df[attr.name].values.astype(np.int64)
        elif attr.type == datapb.DataType.FLOAT:
            df[attr.name] = df[attr.name].values.astype(np.float64)
        else:
            df[attr.name] = [t.strip()
                             for t in df[attr.name].values.astype(np.str)]
    name = path.split('/')[-1].replace('.csv', '')
    return data.Table(name, schema, df)


def get_data(cfg_data):
    if cfg_data.root == '':
        return None

    if cfg_data.type == 'csv':
        data = load_csv(cfg_data.root, cfg_data.primary_key,
                        cfg_data.schema, cfg_data.types)
    else:
        raise NotImplementedError(
            f"Data type {cfg_data.type} is not implemented.")

    return data
