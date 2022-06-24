from federatedscope.db.model.sqlquery_pb2 import BasicQuery


class SQLScheduler(object):
    def __init__(self):
        pass

    def schedule(self, query: BasicQuery):
        # Judge where to execute the query

        # Step 1: build an AST tree

        # Step 2: execute from bottom and generate schedules

        pass