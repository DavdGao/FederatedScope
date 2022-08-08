def get_encryptor(type, **kwargs):
    if type == '':
        return None
    elif type == 'mda_encryptor':
        from federatedscope.db.encryptor.mda_encryptor import MdaEncryptor
        return MdaEncryptor(**kwargs)
    elif type == 'solh_encryptor':
        from federatedscope.db.encryptor.solh_encryptor import SOLHEncryptor
        return SOLHEncryptor(**kwargs)
    else:
        raise NotImplementedError(f"Encryptor {type} not implement.")
