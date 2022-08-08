from federatedscope.db.algorithm.ldp import LDPOLH

class SOLHEncryptor:
    def __init__(self, epsilon):
        self.eps = epsilon
        self.ldp = LDPOLH(epsilon)

    def encode_table(self, table):
        """
        encode table with solh

        Args:
            table (accessor.Table): table to be encoded
            eps (float): ldp epsilon parameter

        Returns:
            encoded table
        """
        
        encoded_table = self.ldp.encode_table(table)
        return encoded_table