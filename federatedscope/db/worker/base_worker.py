from federatedscope.core.communication import gRPCCommManager

class Worker(object):
    """
    The base worker class.
    """
    def __init__(self, ID, host, port, config=None):
        self._ID = ID
        self._cfg = config
        self.local_address = {
            'host': host,
            'port': port
        }

        self.msg_handlers = dict()
        self.comm_manager = gRPCCommManager(host=host, port=port, client_num=2)

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    def register_handlers(self, msg_type, callback_func):
        self.msg_handlers[msg_type] = callback_func