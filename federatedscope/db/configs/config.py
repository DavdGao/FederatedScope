from yacs.config import CfgNode as CN

global_cfg = CN()

def init_global_cfg(cfg):
    cfg.role = ''

    # ------------------------------------------------------------------------ #
    # Dataset related options
    # ------------------------------------------------------------------------ #
    cfg.data = CN()

    cfg.data.root = ''
    cfg.data.type = ''
    # If the `cfg.data.type` is csv, the user need to provide schema and types by config
    cfg.data.primary_key = ''
    cfg.data.schema = []
    cfg.data.types = []

    # ------------------------------------------------------------------------ #
    # Server related options
    # ------------------------------------------------------------------------ #
    cfg.server = CN()

    cfg.server.host = '0.0.0.0'
    cfg.server.port = 50050
    cfg.server.merge = ''

    # ------------------------------------------------------------------------ #
    # Client related options
    # ------------------------------------------------------------------------ #
    cfg.client = CN()

    cfg.client.host = '0.0.0.0'
    cfg.client.port = 50050
    cfg.client.upload_data = False

    # ------------------------------------------------------------------------ #
    # Distribute training related options
    # ------------------------------------------------------------------------ #
    cfg.distribute = CN()

    cfg.distribute.grpc_max_send_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_max_receive_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_enable_http_proxy = False

init_global_cfg(global_cfg)