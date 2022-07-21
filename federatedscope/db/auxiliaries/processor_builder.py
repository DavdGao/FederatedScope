def get_processor(type, **kwargs):
    if type == 'general_processor':
        from federatedscope.db.processor.general_processor import GeneralProcessor
        return GeneralProcessor(**kwargs)
    elif type == 'mda_processor':
        from federatedscope.db.processor.mda_processor import MdaProcessor
        return MdaProcessor(**kwargs)
    else:
        raise NotImplementedError(f"Processor {type} not implement.")
