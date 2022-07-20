from federatedscope.db.register import encryptor_dict

def get_encryptor(config):
    for func in encryptor_dict.values():
        encryptor = func(config)
        if encryptor is not None:
            return encryptor
