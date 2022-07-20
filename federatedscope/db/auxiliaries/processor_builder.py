from federatedscope.db.register import processor_dict


def get_processor(type):
    for func in processor_dict.values():
        processor = func(type)
        if processor is not None:
            return processor
