from federatedscope.db.algorithm.hdtree import LDPHDTree


class MdaEncryptor:
    def __init__(self, eps, fanout):
        self.eps = eps
        self.fanout = fanout

    def encode_table(self, table):
        """
        encode table with hd tree

        Args:
            table (accessor.Table): table to be encoded
            eps (float): ldp epsilon parameter
            fanout (int): hdtree parameter

        Returns:
            (hdtree, encoded table)
        """
        hdtree = LDPHDTree(table.schema.sensitive_attrs(), self.eps,
                           self.fanout)
        encoded_table = hdtree.encode_table(table)
        return hdtree, encoded_table
