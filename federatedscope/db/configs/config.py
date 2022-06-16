from yacs.config import CfgNode as CN

global_cfg = CN()

def init_global_cfg(cfg):
    # ------------------------------------------------------------------------ #
    # Dataset related options
    # ------------------------------------------------------------------------ #
    cfg.data = CN()

    cfg.data.root = "data"

    # ------------------------------------------------------------------------ #
    # Distribute training related options
    # ------------------------------------------------------------------------ #
    cfg.distribute = CN()

    cfg.distribute.role = 'client'
    cfg.distribute.server_host = "0.0.0.0"
    cfg.distribute.server_port = 50050
    cfg.distribute.client_host = '0.0.0.0'
    cfg.distribute.client_port = 50050
    cfg.distribute.grpc_max_send_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_max_receive_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_enable_http_proxy = False

init_global_cfg(global_cfg)