from federatedscope.db.worker.base_worker import Worker
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.aggregator.aggregator import SQLAggregator
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.core.message import Message
from federatedscope.db.worker.handler import HANDLER
from federatedscope.db.data.data import DataSet
import logging
import time

logger = logging.getLogger(__name__)

class Server(Worker):

    def __init__(self, ID, config):
        host = config.server.host
        port = config.server.port
        super(Server, self).__init__(ID, host, port, config)

        self.join_in_client_num = 0

        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_aggregator = SQLAggregator()

        self.data_global = None


    def run(self):
        while True:
            msg = self.comm_manager.receive()
            self.msg_handlers[msg.msg_type](msg)

            time.sleep(1)

        # TODO: handle termination
        logger.info("The server process ends.")
        # self.terminate(msgt_type="finish")


    def callback_funcs_for_join_in(self, message: Message):
        sender, address = message.sender, message.content
        self.join_in_client_num += 1
        sender = self.join_in_client_num

        # Record the client in network topology
        self.comm_manager.add_neighbors(neighbor_id=sender,
                                        address=address)
        # Assign the ID to the client
        logger.info("Register Client #{} ({}:{}) in the federated database.".format(
            sender,
            address['host'],
            address['port'])
        )
        self.comm_manager.send(
            Message(msg_type=HANDLER.ASSIGN_CLIENT_ID,
                    sender=self.ID,
                    receiver=[sender],
                    content=str(sender)))

    def callback_funcs_for_upload_data(self, message: Message):
        sender, data = message.sender, message.content

        # Merge data: hfl for clients and join with server
        if self.data_global is None:
            # The first time merging
            self.data_global = data
        else:
            # TODO: more elegant and feasible
            data = DataSet.from_pb(data)
            self.data_global = self.data_global.set_index(self._cfg.data.primary_key).join(data.set_index(self._cfg.data.primary_key))
