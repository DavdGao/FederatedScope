import math
import random
import xxhash

import federatedscope.db.model.data_pb2 as datapb

def hash(value, seed):
    return xxhash.xxh32(str(value), seed=seed).intdigest()


class LDPOLH(object):
    def __init__(self, eps):
        self._eps = eps
        self._exp = math.exp(eps)
        self._g = int(round(self._exp)) + 1
        self._thres = float(self._g) / (self._exp + self._g - 1)
        self._p = self._exp / (self._exp + self._g - 1)
        self._q = 1.0 / self._g
        self._fq0 = (-1.0 * self._q) / (self._p - self._q)
        self._fq1 = (1.0 - 1.0 * self._q) / (self._p - self._q)
        self._max_seed = 2147483647
        random.seed()

    def encodes(self, value):
        """
        encode value into OLH report
        Args:
            value: value to be encoded

        Returns:
            tuple(int, int): left is the random seed, right is the hash result
        """
        threshold = random.random()
        h = random.randint(0, self._max_seed)
        if threshold < self._thres:
            return (h, random.randint(0, self._g - 1))
        else:
            x = hash(value, h) % self._g
            return (h, x)

    def decodes(self, report, key):
        """
        decode OLH report
        Args:
            report (tuple(int, int)): left is the random seed, right is the hash result
            key: the target value
        """
        (h, x) = report
        r = hash(key, h) % self._g
        if r == x:
            return self._fq1
        else:
            return self._fq0

    def encode_table(self, table):
        unsensitive_attrs = table.schema.unsensitive_attrs()
        sensitive_attrs = table.schema.sensitive_attrs()
        encoded_table = datapb.Table()
        encoded_table.name = table.name
        encoded_table.data.schema.attributes.extend(table.schema.unsensitive_attrs())
        encoded_table.data.schema.attributes.extend(table.schema.sensitive_attrs())
        for i, row in table.data.iterrows():
            rowpb = encoded_table.data.rows.rows.add()
            for attr in unsensitive_attrs:
                cellpb = rowpb.cells.add()
                if attr.type == datapb.DataType.INT:
                    cellpb.i = row[attr.name]
                elif attr.type == datapb.DataType.FLOAT:
                    cellpb.f = row[attr.name]
                else:
                    cellpb.s = row[attr.name]
            for attr in sensitive_attrs:
                cellpb = rowpb.cells.add()
                cellpb.s = str(self.encodes(row[attr.name]))
        return encoded_table

    def decode_table(self, table, attr_name: str, value):
        cnt = 0.0
        for i, row in table.data.iterrows():
            cnt += self.decodes(eval(row[attr_name]), str(value))
        return cnt