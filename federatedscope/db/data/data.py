import pandas as pd
import numpy as np
import federatedscope.db.model.data_pb2 as datapb


class Schema(object):
    """
    Wrapper of protocol buffer Schema
    Arguments:
        schemapb: The protocol buffer Schema
    """

    def __init__(self, schemapb):
        self.schemapb = schemapb

    def names(self):
        names = []
        for attr in self.schemapb.attributes:
            names.append(attr.name)
        return names

    def attrs(self):
        return self.schemapb.attributes

    def name(self, index):
        return self.schemapb.attributes[index]

    def to_pb(self):
        return self.schemapb


class DataSet(object):
    def __init__(self, schema, raw_data):
        self.schema = schema
        self.data = raw_data

    def schema(self):
        return self.schema

    def to_pb(self):
        return pandas_to_protocol(self.data, self.schema.to_pb())

    def from_pb(datasetpb):
        return DataSet(Schema(datasetpb.schema), protocol_to_pandas(datasetpb.schema, datasetpb.rows))


class Table(object):
    def __init__(self, name, schema, raw_data):
        self.name = name
        self.schema = schema
        self.data = raw_data

    def schema(self):
        return self.schema

    def get_row(self, row_idx: int):
        return self.data[row_idx]

    def join(self, data):
        # TODO: more feasible
        pass

    def to_pb(self):
        datasetpb = pandas_to_protocol(self.data, self.schema.to_pb())
        tablepb = datapb.Table()
        tablepb.name = self.name
        # todo: optimize and avoid copy dataset
        tablepb.data.CopyFrom(datasetpb)
        return tablepb

    def from_pb(tablepb):
        return Table(tablepb.name, Schema(tablepb.data.schema), protocol_to_pandas(tablepb.data.schema, tablepb.data.rows))


def pandas_to_protocol(df, schemapb):
    """
    convert pandas dataframe to protocol buffer DataSet
    """
    dataset = datapb.DataSet()
    dataset.schema.CopyFrom(schemapb)
    for rowid, data in df.iterrows():
        row = dataset.rows.rows.add()
        i = 0
        for attr in schemapb.attributes:
            cell = row.cells.add()
            if attr.type == datapb.DataType.INT:
                cell.i = data[i]
            elif attr.type == datapb.DataType.FLOAT:
                cell.f = data[i]
            else:
                cell.s = data[i]
            i = i + 1
    return dataset


def protocol_to_pandas(schemapb, rowspb):
    """
    convert protocol buffuffer DataSet into pandas dataframe
    """
    schema = Schema(schemapb)
    rows = []
    for rowpb in rowspb.rows:
        row = []
        i = 0
        for cellpb in rowpb.cells:
            if schemapb.attributes[i].type == datapb.DataType.INT:
                row.append(cellpb.i)
            elif schemapb.attributes[i].type == datapb.DataType.FLOAT:
                row.append(cellpb.f)
            else:
                row.append(cellpb.s)
            i = i + 1
        rows.append(row)
    return pd.DataFrame(rows, columns=schema.names())


def parse_attribute(attr):
    """
    parse attribute object into protocol buffer Attribute
    Args:
        attr: a dictionary describing attribute information, format:
        {
            'name': attribute_name,
            'type': data_type(int|float|string),
            'min': min_value(optional),
            'max': max_value(optional),
            'delta': value_interval(optional)
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
        schema_str (string): schema of the csv file in string, format:
            [
                {
                    'name': attribute_name,
                    'type': data_type(int|float|string),
                    'min': min_value(optional),
                    'max': max_value(optional),
                    'delta': value_interval(optional)
                },
                ...
            ]

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
    return Schema(schema)




def load_csv(path, schema_str):
    """
    load a csv file 
    Args:
        path (string): the path to the csv file (use file name as table name)
        schema_str (string): see parse_schema
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
    return Table(name, schema, df)


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
