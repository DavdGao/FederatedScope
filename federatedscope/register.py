import os
import logging

logger = logging.getLogger(__name__)


def register(key, module, module_dict):
    if key in module_dict:
        logger.warning(
            'Key {} is already pre-defined, overwritten.'.format(key))
    module_dict[key] = module


data_dict = {}


def register_data(key, module):
    register(key, module, data_dict)


model_dict = {}


def register_model(key, module):
    register(key, module, model_dict)


trainer_dict = {}


def register_trainer(key, module):
    register(key, module, trainer_dict)


config_dict = {}


def register_config(key, module):
    register(key, module, config_dict)


metric_dict = {}


def register_metric(key, module):
    register(key, module, metric_dict)


criterion_dict = {}


def register_criterion(key, module):
    register(key, module, criterion_dict)


regularizer_dict = {}


def register_regularizer(key, module):
    register(key, module, regularizer_dict)


auxiliary_data_loader_PIA_dict = {}


def register_auxiliary_data_loader_PIA(key, module):
    register(key, module, auxiliary_data_loader_PIA_dict)


splitter_dict = {}


def register_splitter(key, module):
    register(key, module, splitter_dict)


transform_dict = {}


def register_transform(key, module):
    register(key, module, transform_dict)


#### new
COMPONENTS = [
    'trainers',
    'models',
    'dataset',
    'metrics',
    'criterions',
    'aggregators',
    'optimizers',
    'regularizers'
    'workers',
    'splitters'
]

FIELDS = [
    'core',
    'cv',
    'nlp',
    'mf',
    'gfl',
]


# path_dir = os.path.join(os.path.curdir, 'federatedscope', field, component)
def search_cls_in_dir(path_dir):
    for file in os.listdir(path_dir):
        path_file = os.path.join(path_dir, file)
        if os.path.isdir(path_file):
            new_cls = search_cls_in_file(path_file)
        elif file.endswith('.py'):
            new_cls = search_cls_in_file(path_file)
        else:
            pass

def search_cls_in_file(path_file):
    cls_dict = dict()
    with open(path_file, 'r') as file:
        for line in file:
            if line.startswith('class '):

                cls_name = line.strip()
                package = ''
                cls_dict[cls_name] = package
    return cls_dict


def merge_cls_dict(dict1, dict2):
    # Repeated names
    repeated_cls = set(dict1.keys()) & set(dict2.keys())
    if len(repeated_cls) > 0:
        repeated_pairs = ', '.join([f'{dict1[cls_name]}.{cls_name}:{dict2[cls_name]}.{cls_name}' for cls_name in repeated_cls])
        raise NameError(f'Repeated class for {repeated_pairs}')

    return dict(**dict1, **dict2)

''.