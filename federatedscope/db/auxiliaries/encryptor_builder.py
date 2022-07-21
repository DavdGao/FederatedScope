def get_encryptor(type, **kwargs):
    if type is '':
        return None
    elif type == 'mda_encryptor':
        from federatedscope.db.encryptor.mda_encryptor import MdaEncryptor
        return MdaEncryptor(**kwargs)
    else:
        raise NotImplementedError(f"Encryptor {type} not implement.")
