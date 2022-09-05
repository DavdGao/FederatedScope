from distutils.command.upload import upload
from federatedscope.db.worker.handler import HANDLER
import logging

from federatedscope.core.message import Message
from federatedscope.db.enums import ROLE
from federatedscope.db.worker.base_worker import Worker
from federatedscope.db.accessor.data import Table
import federatedscope.db.model.data_pb2 as datapb
import time
from google.protobuf import text_format

logger = logging.getLogger(__name__)


class Shuffler(Worker):
    def __init__(self, ID, server_id, config):
        host = config.shuffler.host
        port = config.client.port
        super(Shuffler, self).__init__(ID, host, port, config)

        self.info['role'] = ROLE.SHUFFLER

        self.server_id = server_id

        self.comm_manager.add_neighbors(neighbor_id=server_id,
                                        address={
                                            'host': self._cfg.server.host,
                                            'port': self._cfg.server.port
                                        })
        self.clients_in_charge = None

    def join_in(self):
        """
        To send 'join_in' message to the server for joining in the FL course.
        """
        logger.info(f"Send register request to Server #{self.server_id}.")
        self.comm_manager.send(
            Message(msg_type=HANDLER.JOIN_IN,
                    sender=self.ID,
                    receiver=[self.server_id],
                    content=self.info))

    def run(self):
        """
        To listen to the message and handle them accordingly  (used for distributed mode)
        """
        # Join the federated network as a shuffler
        self.join_in()
        self.listen_remote()

    def listen_remote(self):
        logger.info("The shuffler begins to listen to the remote client")
        while True:
            msg = self.comm_manager.receive()
            self.msg_handlers[msg.msg_type](msg)
            if msg.msg_type == 'finish':
                break
            time.sleep(1)
        logger.info("The shuffler process ends.")

    def callback_funcs_for_assign_id(self, message):
        content = message.content
        self.ID = int(content['ID'])
        logger.info(
            'Shuffler (address {}:{}) is assigned with #{:d}.'.format(
                self.comm_manager.host, self.comm_manager.port, self.ID))

    def update_clients_in_charge(self, new_clients_info):
        if self.clients_in_charge is not None:
            logger.info(
                f'The assigned clients are updated with IDs {list(new_clients_info.keys())}.')
            overlap = self.clients_in_charge.keys()
        else:
            logger.info(
                f'Receive assigned client with IDs {list(new_clients_info.keys())}.')
            self.clients_in_charge = new_clients_info

    def callback_funcs_for_assign_clients(self, message):
        """
        Receive assigned clients from the server
        """
        content = message.content
        if self.clients_in_charge is not None:
            logger.info(
                f'The assigned clients are updated with IDs {list(content.keys())}.')
            self.update_clients_in_charge(content)
        else:
            logger.info(
                f'Receive assigned client with IDs {list(content.keys())}.')
        self.clients_in_charge = content

    def callback_funcs_for_upload_data(self, message: Message):
        sender, data = message.sender, message.content
        tablepb = text_format.Parse(data, datapb.Table())
        table = Table.from_pb(tablepb)
        logger.info(f'Receive encoded table from Client {sender} with config {tablepb.config}.')
        # todo: check consistency of config
        self.config = tablepb.config
        if self.data_global is None:
            self.data_global = table
        else:
            self.data_global.concat(table)
        self.data_global.data.sample(frac=1).reset_index(drop=True)
        self.upload_data()

    def upload_data(self):
        """
        Upload encrypted accessor to the server
        """
        logger.info(f"Send encrypted data to the server with {self._cfg.processor}.")
        # todo: serialize into bytes to reduce storage space usage
        tablepb = self.data_global.to_pb()
        tablepb.config = self.config
        self.comm_manager.send(
            Message(msg_type=HANDLER.UPLOAD_DATA,
                    sender=self.ID,
                    receiver=[self.server_id],
                    content=str(tablepb)))