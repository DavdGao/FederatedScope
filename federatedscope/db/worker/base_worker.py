from federatedscope.core.communication import gRPCCommManager
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.processor.external_processor import ExternalSQLProcessor
from federatedscope.db.processor.local_processor import LocalSQLProcessor
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.db.worker.handler import HANDLER
from federatedscope.db.data.csv_accessor import get_data
from federatedscope.db.interface import Interface

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

        # SQL attribute
        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_processor_external = ExternalSQLProcessor()
        self.sql_processor_local = LocalSQLProcessor()

        self.msg_handlers = dict()
        self._register_default_handlers()

        logger.info('{}: Listen to {}:{}...'.format(self._cfg.role, host, port))
        self.comm_manager = gRPCCommManager(host=host, port=port, client_num=2)

        # Load data
        self.data = get_data(self._cfg.data)

        if config.local_query:
            self.interface = Interface()

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    def listen_local(self):
        logger.info("The server is waiting for input query.")

        for statement in self.interface.get_input():
            # Check if the statement is legal
            if not self.sql_parser.check_syntax(statement):
                continue
            # Construct query
            query = self.sql_parser.parse(statement)
            print(query)
            res_local = self.sql_processor_local.mda_query(query, 1.01, 5)

            # Print in the terminal
            self.interface.print(res_local)

        logger.info("The server is waiting for input query.")

    def _register_default_handlers(self):
        for handler in HANDLER.values():
            func_handler = "callback_funcs_for_{}".format(handler.lower())
            if hasattr(self, func_handler):
                self.register_handlers(handler, getattr(self, func_handler))

    def register_handlers(self, msg_type, callback_func):
        self.msg_handlers[msg_type] = callback_func
