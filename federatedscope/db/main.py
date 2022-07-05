import sys
import os

# TODO: modified it
DEV_MODE = True  # simplify the federatedscope re-setup everytime we change the source codes of federatedscope
if DEV_MODE:
    # file_dir = os.path.join(os.path.dirname(__file__), '../..')
    sys.path.append('/mnt/gaodawei.gdw/FederatedScope')

from federatedscope.db.configs.config import global_cfg
from federatedscope.db.worker.client import Client
from federatedscope.db.worker.server import Server
from federatedscope.core.cmd_args import parse_args

import logging

logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    init_cfg = global_cfg.clone()
    args = parse_args()
    init_cfg.merge_from_file(args.cfg_file)
    init_cfg.merge_from_list(args.opts)

    if init_cfg.role == "client":
        worker = Client(ID=-1,
                        server_id=0,
                        config=init_cfg)
    elif init_cfg.role == "server":
        worker = Server(ID=0, config=init_cfg)

    worker.run()
