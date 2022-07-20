from federatedscope.db.register import processor_dict


def get_processor(config):
    for func in processor_dict.values():
        processor = func(config)
        if processor is not None:
            return processor
