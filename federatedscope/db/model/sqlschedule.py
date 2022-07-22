import federatedscope.db.model.sqlquery_pb2 as querypb
import federatedscope.db.model.data_pb2 as datapb


class Query(object):
    def __init__(self, querypb):
        self.querypb = querypb

    def target_table_name(self):
        return self.querypb.table_name

