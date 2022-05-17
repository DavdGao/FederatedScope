from federatedscope.db.worker.base_worker import Worker
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.aggregator.aggregator import SQLAggregator
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.core.message import Message


class Server(Worker):
    def __init__(self, ID, host, port, config):
        super(Server, self).__init__(ID, host, port, config)

        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_aggregator = SQLAggregator()

    def callback_funcs_for_join_in(self, message: Message):
        sender, address = message.sender, message.content
        self.join_in_client_num += 1
        sender = self.join_in_client_num

        # Record the client in network topology
        self.comm_manager.add_neighbors(neighbor_id=sender,
                                        address=address)
        # Assign the ID to the client
        self.comm_manager.send(
            Message(msg_type="assign_client_id",
                    sender=self.ID,
                    receiver=[sender],
                    content=str(sender)))
