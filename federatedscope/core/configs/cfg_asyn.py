import logging

from federatedscope.core.configs.config import CN
from federatedscope.register import register_config


def extend_asyn_cfg(cfg):
    # ------------------------------------------------------------------------ #
    # Asynchronous related options
    # ------------------------------------------------------------------------ #
    cfg.asyn = CN()

    cfg.asyn.use = False
    cfg.asyn.timeout = 0
    cfg.asyn.min_received_num = 2
    cfg.asyn.min_received_rate = -1.0

    # --------------- register corresponding check function ----------
    cfg.register_cfg_check_fun(assert_asyn_cfg)


def assert_asyn_cfg(cfg):
    # to ensure a valid timeout seconds
    pass


register_config("asyn", extend_asyn_cfg)
