def wrap_attacker_trainer(base_trainer, config):
    '''Wrap the trainers for attack client.
    Args:
        base_trainer (core.trainers.GeneralTorchTrainer): the trainers that
        will be wrapped;
        config (federatedscope.core.configs.config.CN): the configure;

    :returns:
        The wrapped trainers; Type: core.trainers.GeneralTorchTrainer

    '''
    if config.attack.attack_method.lower() == 'gan_attack':
        from federatedscope.attack.trainer import wrap_GANTrainer
        return wrap_GANTrainer(base_trainer)
    elif config.attack.attack_method.lower() == 'gradascent':
        from federatedscope.attack.trainer import wrap_GradientAscentTrainer
        return wrap_GradientAscentTrainer(base_trainer)
    elif config.attack.attack_method.lower() == 'backdoor':
        from federatedscope.attack.trainer import wrap_backdoorTrainer
        return wrap_backdoorTrainer(base_trainer)
    else:
        raise ValueError('Trainer {} is not provided'.format(
            config.attack.attack_method))
