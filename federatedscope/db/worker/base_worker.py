from federatedscope.core.communication import gRPCCommManager

from federatedscope.db.auxiliaries.processor_builder import get_processor
from federatedscope.db.auxiliaries.encryptor_builder import get_encryptor
from federatedscope.db.auxiliaries.parser_builder import get_parser
from federatedscope.db.auxiliaries.accessor_builder import get_accessor
from federatedscope.db.worker.handler import HANDLER
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
        self.local_address = {'host': host, 'port': port}

        # SQL attribute
        self.sql_parser = get_parser(**self._cfg.parser)
        # TODO: implement for distribute query
        # self.sql_scheduler = SQLScheduler()
        self.sql_encryptor = get_encryptor(**self._cfg.encryptor)
        self.sql_processor = get_processor(**self._cfg.processor)

        self.msg_handlers = dict()
        self._register_default_handlers()

        logger.info('{}: Listen to {}:{}...'.format(self._cfg.role, host,
                                                    port))
        self.comm_manager = gRPCCommManager(host=host, port=port, client_num=2)

        # Data accessor
        self.sql_accessor = get_accessor(**self._cfg.accessor)
        self.data_global = None

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
            if self.data_global == None:
                logger.info("Global table not exists.")
            else:
                # TODO: why external here?
                res_local = self.sql_processor.execute(
                    query, self.sql_accessor.get_table())
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
