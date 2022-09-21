import logging

from federatedscope.core.configs.config import CN
from federatedscope.register import register_config
from federatedscope.core.auxiliaries.enums import PROTOCOL

logger = logging.getLogger(__name__)


def extend_consult_cfg(cfg):
    cfg.consult = CN()

    cfg.consult.use = False
    cfg.consult.info_request_by_server = [] # what we request from the client
    cfg.consult.info_request_by_client = [] # what we request from the server


def assert_consult_cfg(cfg):
    if cfg.consult.use:
        for info in cfg.consult.info_request_by_server:
            assert info in PROTOCOL, f"{info} in cfg.consult.info_request_by_server is not supported."

        for info in cfg.consult.info_request_by_client:
            assert info in PROTOCOL, f"{info} in cfg.consult.info_request_by_client is not supported."


register_config('consult', extend_consult_cfg)
