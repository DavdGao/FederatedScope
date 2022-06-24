from federatedscope.db.worker.base_worker import Worker
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.aggregator.aggregator import SQLAggregator
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.core.message import Message
from federatedscope.db.worker.handler import HANDLER
import logging
import time

logger = logging.getLogger(__name__)

class Server(Worker):

    def __init__(self, ID, config):
        host = config.distribute.server_host
        port = config.distribute.server_port
        super(Server, self).__init__(ID, host, port, config)

        self.join_in_client_num = 0

        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_aggregator = SQLAggregator()

        self.data_all = None

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
        if self.data_all is None:
            # The first time merging
            if self.data is None:
                self.data_all = data
            else:
                # Join the data from client
                self.data_all = self.data.join(data)
        else:
            # Suppose it is equal join
            self.data_all.join(data)

