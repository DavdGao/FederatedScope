
class Data(object):
    def __init__(self, id, schema, rows):
        self.id = id
        self.schema = schema
        self.rows = rows

    def get_row(self, row_idx: int):
        return self.rows[row_idx]
