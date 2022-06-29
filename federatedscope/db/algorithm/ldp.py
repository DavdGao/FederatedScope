import math
import random
import xxhash

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
        self._fq0 = (- 1.0 * self._q) / (self._p - self._q)
        self._fq1 = (1.0 - 1.0 * self._q) / (self._p - self._q)
        self._max_seed = 2147483647

    def encodes(self, value):
        """
        encode value into OLH report
        Args:
            value: value to be encoded

        Returns:
            tuple(int, int): left is the random seed, right is the hash result
        """
        h = random.randint(0, self._max_seed)
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
        if hash(key, h) == x:
            return self._fq1
        else:
            return self._fq0