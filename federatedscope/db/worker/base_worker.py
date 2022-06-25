from federatedscope.core.communication import gRPCCommManager
from federatedscope.db.worker.handler import HANDLER
from federatedscope.db.data.data import get_data

import logging

logger = logging.getLogger(__name__)


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
        self._register_default_handlers()

        logger.info('{}: Listen to {}:{}...'.format(self._cfg.distribute.role, host, port))
        self.comm_manager = gRPCCommManager(host=host, port=port, client_num=2)

        # Load data
        self.data = get_data(self._cfg.data)

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    def _register_default_handlers(self):
        for handler in HANDLER.values():
            func_handler = "callback_funcs_for_{}".format(handler.lower())
            if hasattr(self, func_handler):
                self.register_handlers(handler, getattr(self, func_handler))

    def register_handlers(self, msg_type, callback_func):
        self.msg_handlers[msg_type] = callback_func
