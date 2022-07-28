from yacs.config import CfgNode as CN

global_cfg = CN()


def init_global_cfg(cfg):
    cfg.role = ''
    cfg.local_query = False

    # ------------------------------------------------------------------------ #
    # Dataset related options
    # ------------------------------------------------------------------------ #
    cfg.data = CN()

    # todo: rename to accessor.url may be better
    cfg.data.root = ''
    # If the `cfg.accessor.type` is csv, the user need to provide schema and types by config
    cfg.data.type = ''
    cfg.data.schema = []

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
    # Shuffler related options
    # ------------------------------------------------------------------------ #
    cfg.shuffler = CN()

    cfg.shuffler.host = '0.0.0.0'
    cfg.shuffler.port = 50050
    cfg.shuffler.upload_data = False

    # ------------------------------------------------------------------------ #
    # Processor related options
    # ------------------------------------------------------------------------ #
    cfg.processor = CN(new_allowed=True)

    cfg.processor.type = 'general'

    # ------------------------------------------------------------------------ #
    # Encryptor related options
    # ------------------------------------------------------------------------ #
    cfg.encryptor = CN(new_allowed=True)

    cfg.encryptor.type = ''

    # ------------------------------------------------------------------------ #
    # Parser training related options
    # ------------------------------------------------------------------------ #
    cfg.parser = CN()

    cfg.parser.type = ''

    # ------------------------------------------------------------------------ #
    # Distribute training related options
    # ------------------------------------------------------------------------ #
    cfg.distribute = CN()

    cfg.distribute.grpc_max_send_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_max_receive_message_length = 100 * 1024 * 1024
    cfg.distribute.grpc_enable_http_proxy = False


init_global_cfg(global_cfg)
