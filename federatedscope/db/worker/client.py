from federatedscope.db.worker.base_worker import Worker
from federatedscope.core.message import Message
from multiprocessing import Process, Queue
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.processor.local_processor import LocalSQLProcessor
from federatedscope.db.processor.external_processor import ExternalSQLProcessor
from federatedscope.db.aggregator.aggregator import SQLAggregator
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.db.interface import Interface
import federatedscope.db.model.data_pb2 as datapb

import logging

from federatedscope.db.worker.handler import HANDLER

logger = logging.getLogger(__name__)



class Client(Worker):

    def __init__(self, ID, server_id, config):
        host = config.client.host
        port = config.client.port
        super(Client, self).__init__(ID, host, port, config)

        self.server_id = server_id

        self.interface = Interface()

        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_processor_local = LocalSQLProcessor()
        self.sql_aggregator = SQLAggregator()

        # Pass and store the query result from remote client
        # Currently only consider a single query
        self.queue_remote = Queue

        self.comm_manager.add_neighbors(neighbor_id=server_id,
                                        address={
                                            'host': self._cfg.server.host,
                                            'port': self._cfg.server.port
                                        })

    def join_in(self):
        """
        To send 'join_in' message to the server for joining in the FL course.
        """
        logger.info(f"Send register request to Server #{self.server_id}.")
        self.comm_manager.send(
            Message(msg_type=HANDLER.JOIN_IN,
                    sender=self.ID,
                    receiver=[self.server_id],
                    content=self.local_address))

    def upload_data(self):
        """
        Upload encrypted data to the server
        """
        logger.info(f"Send encrypted data to the server with epsilon={self._cfg.ldp.epsilon}, fanout={self._cfg.ldp.fanout}.")
        (_, encoded_table) = self.sql_processor_local.encode_table(self.data, self._cfg.ldp.epsilon, self._cfg.ldp.fanout)
        # todo: serialize into bytes to reduce storage space usage
        self.comm_manager.send(
            Message(msg_type=HANDLER.UPLOAD_DATA,
                    sender=self.ID,
                    receiver=[self.server_id],
                    content=str(encoded_table))
        )

    def run(self):
        """
        To listen to the message and handle them accordingly  (used for distributed mode)
        """
        # Join the federated network
        self.join_in()

        # Upload data if permitted
        if self._cfg.client.upload_data:
            self.upload_data()
        else:
            # Start a remote listener
            p_remote = Process(target=self.listen_remote)
            p_remote.start()
            self.listen_remote()

        if self._cfg.client.local_process:
            # Start a local listener
            # TODO: create a process and share interface among local/remote process
            p_local = Process(target=self.listen_local)
            p_local.start()
            self.listen_local()

    def listen_local(self):
        for statement in self.interface.get_input():
            # Check if the statement is legal
            if not self.sql_parser.check_syntax(statement):
                continue
            # Construct query
            query = self.sql_parser.parse(statement)
            # Construct schedule for the query
            schedule_local, scheduler_remote = self.sql_scheduler.schedule(query)

            # Process the sub-query locally
            res_local = self.sql_processor_local.process(schedule_local)
            # Send the schedule to the corresponding clients
            self.sql_processor_external.send(scheduler_remote)

            # Wait for collecting the results
            while True:
                # Process a remote result
                sub_res_remote = self.queue_remote.get()
                self.sql_processor_external.append(res_remote)
                # Finish the remote sub-query
                if self.sql_processor_external.isfinish():
                    break

            # Obtain the results from remote clients
            res_remote = self.sql_processor_external.aggregate()
            # Obtain the final results
            res = self.sql_aggregator.aggregate(res_local, res_remote)
            # Print in the terminal
            self.interface.print(res)

        # End the process
        self.interface.end()

    def listen_remote(self):
        # Listen for query and result
        while True:
            msg = self.comm_manager.receive()
            self.msg_handlers[msg.msg_type](msg)

            if msg.msg_type == 'finish':
                break

    def callback_funcs_for_query(self, message: Message):
        """
        Receive query request from remote clients

        Args:
            message:

        Returns:

        """
        statement = message.content
        # Construct query
        query = self.sql_parser.parse(statement)
        # Construct local schedule
        schedule_local, _ = self.sql_scheduler.schedule(query)
        res_external = self.sql_processor_external.process(schedule_local)

        self.comm_manager.send(
            Message(msg_type="",
                    sender=self.ID,
                    receiver=message.sender,
                    content=res_external))

    def callback_funcs_for_res(self, message: Message):
        """
        Receive query results from the remote clients

        Args:
            message:

        Returns:

        """
        result = message.content
        self.queue_remote.put(result)

    def callback_funcs_for_update_network(self, message: Message):
        pass

    def callback_funcs_for_assign_client_id(self, message: Message):
        content = message.content
        self.ID = int(content)
        self.interface.print('Client (address {}:{}) is assigned with #{:d}.'.format(
            self.comm_manager.host, self.comm_manager.port, self.ID))
