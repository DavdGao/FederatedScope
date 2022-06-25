import pandas as pd
import federatedscope.db.model.data_pb2 as datapb

class Schema(object):
    def __init__(self, schemapb):
        self.schemapb = schemapb

    def names(self):
        names = []
        for attr in self.schemapb.attribute:
            names.append(attr.name)
        return names

    def name(self, index):
        return self.schemapb.attribute[index]

class Data(object):
    def __init__(self, name, primary, schema, raw_data):
        self.name = name
        self.primary = primary
        self.schema = schema
        self.data = raw_data

    def get_row(self, row_idx: int):
        return self.data[row_idx]

    def join(self, data):
        # TODO: more feasible
        return self.data.join(data.set_index(self.primary), on=self.primary)

    def to_proto(self):
        # TODO: transform into protocol buffer Data
        pass


def parse_attribute(attr):
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
        if  attrpb.type == datapb.DataType.INT:
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
    schema = datapb.Schema()
    attrs = eval(schema_str.strip())
    attrpbs = []
    for attr in attrs:
        if 'name' not in attr:
            raise ValueError("No name in attribute definition")
        if 'type' not in attr:
            raise ValueError("No type in attribute definition")
        attrpbs.append(parse_attribute(attr))
    schema.attribute.extend(attrpbs)
    return schema

# todo: optimize schema config format
def load_csv(root, primary, schema_str, types):
    schema = parse_schema(schema_str)
    csv = pd.read_csv(
        root,
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
    name = root.split('/')[-1].replace('.csv', '')
    return Data(name, primary, schema, csv)


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
