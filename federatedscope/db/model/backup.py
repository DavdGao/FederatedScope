class Filter(object):
    def __init__(self, attr, left, right):
        self.attr = attr
        self.left = left
        self.right = right


class Aggregate(object):
    def __init__(self, attr, func_type):
        self.attr = attr
        self.func_type = func_type


class SQLQuery(object):
    def __init__(self,
                 qid,
                 statement,
                 table_name,
                 filters=None,
                 attrs=[],
                 aggregate=None):
        self.qid = qid
        self.statement = statement
        self.table_name = table_name
        self.filters = filters
        self.attrs = attrs
        self.aggregate = aggregate
