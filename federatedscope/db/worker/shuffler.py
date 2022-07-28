import logging

from federatedscope.core.message import Message
from federatedscope.db.enums import ROLE
from federatedscope.db.worker.base_worker import Worker

logger = logging.getLogger(__name__)

from federatedscope.db.worker.handler import HANDLER


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
                    content=self.local_address))

    def run(self):
        """
        To listen to the message and handle them accordingly  (used for distributed mode)
        """
        # Join the federated network as a shuffler
        self.join_in()

    def callback_funcs_for_assign_id(self, message):
        content = message.content
        self.ID = int(content)
        self.interface.print(
            'Shuffler (address {}:{}) is assigned with #{:d}.'.format(
                self.comm_manager.host, self.comm_manager.port, self.ID))

    def update_clients_in_charge(self, new_clients_info):
        if self.clients_in_charge is not None:
            logger.info(f'The assigned clients are updated with IDs {list(new_clients_info.keys())}.')
            overlap = self.clients_in_charge.keys()
        else:
            logger.info(f'Receive assigned client with IDs {list(new_clients_info.keys())}.')
            self.clients_in_charge = new_clients_info

    def callback_funcs_for_assign_clients(self, message):
        """
        Receive assigned clients from the server
        """
        content = message.content
        if self.clients_in_charge is not None:
            logger.info(f'The assigned clients are updated with IDs {list(content.keys())}.')
            self.update_clients_in_charge(content)
        else:
            logger.info(f'Receive assigned client with IDs {list(content.keys())}.')
        self.clients_in_charge = content



