from federatedscope.db.algorithm.hdtree import LDPHDTree
from federatedscope.db.register import register_encryptor


class MdaEncryptor:
    def __init__(self, eps, fanout):
        self.eps = eps
        self.fanout = fanout

    def encode_table(self, table):
        """
        encode table with hd tree

        Args:
            table (data.Table): table to be encoded
            eps (float): ldp epsilon parameter
            fanout (int): hdtree parameter

        Returns:
            encoded table
        """
        hdtree = LDPHDTree(table.schema.sensitive_attrs(), self.eps, self.fanout)
        # todo: avoid rebuilding hdtree every time
        encoded_table = hdtree.encode_table(table)
        return encoded_table

def call_mda_encryptor(config):
    if config.processor.type == 'mda':
        encryptor = MdaEncryptor(config.processor.eps, config.processor.fanout)
        return encryptor


register_encryptor('mda', call_mda_encryptor)