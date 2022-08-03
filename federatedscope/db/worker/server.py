from federatedscope.db.enums import ROLE
from federatedscope.db.worker.base_worker import Worker

from federatedscope.core.message import Message
from federatedscope.db.worker.handler import HANDLER
from federatedscope.db.accessor.data import Table
import federatedscope.db.model.data_pb2 as datapb
import logging
import time
from threading import Thread
from google.protobuf import text_format

logger = logging.getLogger(__name__)

class RoleManager(dict):
    def __init__(self):
        super(RoleManager, self).__init__()

    def get_shufflers(self):
        return [k for k,v in self.items() if v == ROLE.SHUFFLER]

    def has_shuffler(self):
        return ROLE.SHUFFLER in self.values()


class Server(Worker):
    def __init__(self, ID, config):
        host = config.server.host
        port = config.server.port
        super(Server, self).__init__(ID, host, port, config)

        self.info['role'] = ROLE.SERVER

        self.data_global = None

        self.role_manager = RoleManager()

    def run(self):
        listener = Thread(target=self.listen_remote)
        listener.setDaemon(True)
        listener.start()
        self.listen_local()

    @property
    def join_in_num(self):
        return len(self.role_manager)

    def join_in_role_num(self, role):
        return len([_ for _ in self.role_manager.values() if _ == role])

    def listen_remote(self):
        logger.info("The server begins to listen to the remote clients.")

        while True:
            msg = self.comm_manager.receive()
            self.msg_handlers[msg.msg_type](msg)

            if msg.msg_type == 'finish':
                break

            time.sleep(1)

        # TODO: handle termination
        logger.info("The server process ends.")
        # self.terminate(msgt_type="finish")

    def callback_funcs_for_join_in(self, message: Message):
        sender, info = message.sender, message.content

        role, host, port = info['role'], info['host'], info['port']

        sender = self.join_in_num + 1
        # Record the client in network topology
        self.comm_manager.add_neighbors(neighbor_id=sender, address={'host': host, 'port': port})
        # Record it in role manager
        self.role_manager[sender] = role

        # Assign the ID to the new participant
        logger.info(
            "Register {} #{} ({}:{}) in the federated database.".format(
                role, sender, host, port))

        if role == ROLE.CLIENT and self.role_manager.has_shuffler():
            # TODO: support multiple shufflers
            shuffler_id = self.role_manager.get_shufflers()[0]
            # TODO: assign method
            id_superior = shuffler_id
            host_superior, port_superior = self.comm_manager.get_neighbors(shuffler_id).split(':')
        else:
            id_superior = self.ID
            host_superior, port_superior = self.comm_manager.host, self.comm_manager.port
        content = {'ID': sender, 'ID_superior': id_superior, 'host_superior': host_superior, 'port_superior': port_superior}
        logging.info("content {}".format(str(content)))

        self.comm_manager.send(
            Message(msg_type=HANDLER.ASSIGN_ID,
                    sender=self.ID,
                    receiver=[sender],
                    content=content))

    def callback_funcs_for_upload_data(self, message: Message):
        sender, data = message.sender, message.content
        tablepb = text_format.Parse(data, datapb.Table())
        table = Table.from_pb(tablepb)
        if self._cfg.processor.type == 'mda_processor':
            left_key = self.data_accessor.get_table().schema.primary()
            right_key = table.schema.primary()
            join_table = self.data_accessor.get_table().join(table, left_key.name, right_key.name)
            if self.data_global is None:
                self.data_global = join_table
                self.sql_processor.prepare(self.data_global)
            else:
                self.data_global.concat(join_table)
        else:
            self.data_global = table
