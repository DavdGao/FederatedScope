from federatedscope.auto_register import optimizer_dict
from federatedscope.auto_register import contain

try:
    import torch
except ImportError:
    torch = None

import importlib


def get_scheduler(type, optimizer, **kwargs):
    cls_name, package = contain(type, optimizer_dict)
    if cls_name is not None:
        scheduler_cls = getattr(importlib.import_module(name=cls_name, package=package))
        scheduler = scheduler_cls(optimizer, **kwargs)
    elif torch is None:
        # TODO: create according to the backend
        scheduler = None
    elif hasattr(torch.optim.lr_scheduler, type):
        scheduler = getattr(torch.optim.lr_scheduler, type)(optimizer, **kwargs)
    else:
        raise NotImplementedError(f'Learning rate scheduler {type} not implement')

    return scheduler
