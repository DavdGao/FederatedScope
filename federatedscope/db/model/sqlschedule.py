
class SQLSchedule(object):
    def __init__(self, id, sub_query, target_client):
        self.id = id
        self.sub_query = sub_query
        self.target_client = target_client
        self.result = None

    def set_result(self, result):
        self.result = result

    def is_finished(self):
        return self.result is not None
