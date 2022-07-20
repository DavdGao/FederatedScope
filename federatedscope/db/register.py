import logging

logger = logging.getLogger(__name__)


def register(key, module, module_dict):
    if key in module_dict:
        logger.warning(
            'Key {} is already pre-defined, overwritten.'.format(key))
    module_dict[key] = module


processor_dict = {}
encryptor_dict = {}


def register_processor(key, module):
    register(key, module, processor_dict)

def register_encryptor(key, module):
    register(key, module, encryptor_dict)
