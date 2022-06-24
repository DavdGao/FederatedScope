import pandas as pd

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





def load_csv(root, primary, schema, types):
    csv = pd.read_csv(
        root,
        sep=",",
        engine="python",
        names=schema,
        dtype=types
    )
    name = root.split('/')[-1].replace('.csv', '')
    return Data(name, primary, schema, csv)



def get_data(cfg_data):
    if cfg_data.root == '':
        return None

    if cfg_data.type == 'csv':
        data = load_csv(cfg_data.root, cfg_data.primary_key, cfg_data.schema, cfg_data.types)
    else:
        raise NotImplementedError(f"Data type {cfg_data.type} is not implemented.")

    return data
