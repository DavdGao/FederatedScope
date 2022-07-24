from federatedscope.db.algorithm.hdtree import LDPHDTree
from federatedscope.db.register import register_encryptor


class MdaEncryptor:
    def __init__(self, epsilon, fanout):
        self.eps = epsilon
        self.fanout = fanout

    def encode_table(self, table):
        """
        encode table with hd tree

        Args:
            table (accessor.Table): table to be encoded
            eps (float): ldp epsilon parameter
            fanout (int): hdtree parameter

        Returns:
            encoded table
        """
        hdtree = LDPHDTree(table.schema.sensitive_attrs(), self.eps,
                           self.fanout)
        encoded_table = hdtree.encode_table(table)
        return encoded_table