import math
import random
import xxhash

def hash(value, seed):
    return xxhash.xxh32(str(value), seed=seed).intdigest()

class LDPOracle(object):
    _eps = 1.0
    _exp = None
    _serialized = True

    def __init__(self, eps):
        self._eps = eps
        self._exp = math.exp(eps)
    
    def encodes(self, value, **kwargs):
        raise NotImplementedError

    def decodes(self, report, **kwargs):
        raise NotImplementedError

    def aggregate_new_buffer(self):
        raise NotImplementedError
        
    def aggregate_iterate(self, buffer, report, **kwargs):
        raise NotImplementedError

    def aggregate_merge(self, buffer, pbuffer):
        raise NotImplementedError

    def aggregate_terminate(self, buffer):
        raise NotImplementedError

class LDPOLH(LDPOracle):
    def __init__(self, eps):
        super(LDPOLH, self).__init__(eps)
        self._g = int(round(math.exp(eps))) + 1
        self._thres = float(self._g) / (self._exp + self._g - 1)
        self._p = self._exp / (self._exp + self._g - 1)
        self._q = 1.0 / self._g
        self._fq0 = (- 1.0 * self._q) / (self._p - self._q)
        self._fq1 = (1.0 - 1.0 * self._q) / (self._p - self._q)

    def encodes(self, value):
        h = random(self._g)
        x = hash(value, h) % self.g
        return (hash_seed, x)

    def decodes(self, report, key):
        (h, x) = report
        if hash(key, h) == x:
            return self._fq1
        else:
            return self._fq0