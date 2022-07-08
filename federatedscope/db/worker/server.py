from federatedscope.db.worker.base_worker import Worker
from federatedscope.db.parser.parser import SQLParser
from federatedscope.db.processor.external_processor import ExternalSQLProcessor
from federatedscope.db.scheduler.scheduler import SQLScheduler
from federatedscope.core.message import Message
from federatedscope.db.worker.handler import HANDLER
from federatedscope.db.data.data import Table
from federatedscope.db.model.sqlschedule import Query
import federatedscope.db.model.data_pb2 as datapb
import federatedscope.db.model.sqlquery_pb2 as querypb
from multiprocessing import Process
import logging
import time
from google.protobuf import text_format

logger = logging.getLogger(__name__)

class Server(Worker):

    def __init__(self, ID, config):
        host = config.server.host
        port = config.server.port
        super(Server, self).__init__(ID, host, port, config)

        self.join_in_client_num = 0

        self.sql_parser = SQLParser()
        self.sql_scheduler = SQLScheduler()
        self.sql_processor_external = ExternalSQLProcessor()

        self.data_global = None
        self.join_key = self.data.schema.primary()
        self.generate_demo_query()

    def generate_demo_query(self):
        q = querypb.BasicSchedule()
        q.table_name = "server"
        # SUM(purchase)
        agg = q.exp_agg.add()
        agg.operator = querypb.Operator.SUM # the aggregation type
        agg_attr = agg.children.add()
        agg_attr.operator = querypb.Operator.REF
        agg_attr.s = "purchase"
        # where expressions
        # age >= 30 and age <= 40
        fi = q.exp_where.add()
        fi.operator = querypb.Operator.GE
        attr = fi.children.add()
        attr.operator = querypb.Operator.REF
        attr.s = "age"
        value = fi.children.add()
        value.operator = querypb.Operator.LIT
        value.i = 30
        fi = q.exp_where.add()
        fi.operator = querypb.Operator.LE
        attr = fi.children.add()
        attr.operator = querypb.Operator.REF
        attr.s = "age"
        value = fi.children.add()
        value.operator = querypb.Operator.LIT
        value.i = 40
        # salary >= 50 and salary <= 150
        fi = q.exp_where.add()
        fi.operator = querypb.Operator.GE
        attr = fi.children.add()
        attr.operator = querypb.Operator.REF
        attr.s = "salary"
        value = fi.children.add()
        value.operator = querypb.Operator.LIT
        value.i = 50
        fi = q.exp_where.add()
        fi.operator = querypb.Operator.LE
        attr = fi.children.add()
        attr.operator = querypb.Operator.REF
        attr.s = "salary"
        value = fi.children.add()
        value.operator = querypb.Operator.LIT
        value.i = 150
        self.demo_query = Query(q)

    def run(self):
        # listen to remote gRPC request
        # p_remote = Process(target=self.listen_remote)
        # p_remote.start()

        if self._cfg.local_query:
            self.listen_local()


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
        tablepb = text_format.Parse(data, datapb.Table())
        table = Table.from_pb(tablepb)
        right_key = table.schema.primary()
        join_table = self.data.join(table, self.join_key.name, right_key.name)
        if self.data_global is None:
            self.data_global = join_table
        else:
            self.data_global.concat(join_table)
        print ("mda query SUM(purchase) where age >= 30 and age <= 40 and salary >= 50 and salary <= 150")
        print (self.sql_processor_external.mda_query(self.demo_query, self.data_global, self._cfg.ldp.epsilon, self._cfg.ldp.fanout))