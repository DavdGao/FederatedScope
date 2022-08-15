import torch


class CharacterLoss(object):
    """
    Character_loss from FedEM:
    https://github.com/omarfoq/FedEM/blob/ \
    13f366c41c14b234147c2662c258b8a9db2f38cc/utils/utils.py
    """
    CHARACTERS_WEIGHTS = {
        '\n': 0.43795308843799086,
        ' ': 0.042500849608091536,
        ',': 0.6559597911540539,
        '.': 0.6987226398690805,
        'I': 0.9777491725556848,
        'a': 0.2226022051965085,
        'c': 0.813311655455682,
        'd': 0.4071860494572223,
        'e': 0.13455606165058104,
        'f': 0.7908671114133974,
        'g': 0.9532922255751889,
        'h': 0.2496906467588955,
        'i': 0.27444893060347214,
        'l': 0.37296488139109546,
        'm': 0.569937324017103,
        'n': 0.2520734570378263,
        'o': 0.1934141300462555,
        'r': 0.26035705948768273,
        's': 0.2534775933879391,
        't': 0.1876471355731429,
        'u': 0.47430062920373184,
        'w': 0.7470615815733715,
        'y': 0.6388302610200002
    }

    ALL_LETTERS = "\n !\"&'(),-.0123456789:;>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[" \
                  "]abcdefghijklmnopqrstuvwxyz}"

    def __init__(self, device):
        super(CharacterLoss, self).__init__()

        labels_weight = torch.ones(len(self.ALL_LETTERS), device=device)
        for character in self.CHARACTERS_WEIGHTS:
            labels_weight[self.ALL_LETTERS.index(
                character)] = self.CHARACTERS_WEIGHTS[character]
        self.criterion = torch.nn.CrossEntropyLoss(weight=labels_weight*8).to(device)

    def forward(self, *args, **kwargs):
        return self.criterion(*args, **kwargs)
