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

    def sensitive_attrs(self):
        return list(filter(lambda attr : attr.sensitive, self.schemapb.attributes))

    def unsensitive_attrs(self):
        return list(filter(lambda attr : not attr.sensitive, self.schemapb.attributes))

    def sensitive_attr_names(self):
        return list(map(lambda attr : attr.name, self.sensitive_attrs()))

    def name(self, index):
        return self.schemapb.attributes[index]

    def to_pb(self):
        return self.schemapb


class DataSet(object):
    def __init__(self, schema, raw_data):
        self.schema = schema
        self.data = raw_data

    def to_pb(self):
        return pandas_to_protocol(self.data, self.schema.to_pb())

    def from_pb(datasetpb):
        return DataSet(Schema(datasetpb.schema), protocol_to_pandas(datasetpb.schema, datasetpb.rows))


class Table(object):
    def __init__(self, name, schema, raw_data):
        self.name = name
        self.schema = schema
        self.data = raw_data

    def get_row(self, row_idx: int):
        return self.data[row_idx]

    def join(self, data):
        # TODO: more feasible
        pass

    def project(self, attr_names):
        return self.data[attr_names]

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


