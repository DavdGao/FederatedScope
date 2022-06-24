import random
import math
import hashlib


class SuperEnum(object):
    """
    A data type for enumeration
    https://codereview.stackexchange.com/questions/109724/yet-another-lightweight-enum-for-python-2-7
    """

    class __metaclass__(type):
        def __iter__(self):
            for item in self.__dict__:
                if item == self.__dict__[item]:
                    yield item


class UniversalHashType(SuperEnum):
    """
    Different types of universal hashing
    """
    OriginalInt = 1
    FastInt = 2
    MD5 = 3


class UniversalHash(object):
    """
    Universal hashing for integers:\n
    h(x,a,b) = ((a*x + b) mod p) mod m\n
    x is key you want to hash\n
    a is any number you can choose between 1 to p-1 inclusive\n
    b is any number you can choose between 0 to p-1 inclusive\n
    p is a prime number that is greater than max possible value of x\n
    m is a max possible value you want for hash code + 1\n
    \n
    (unsigned) (aa*x + bb) >> (w - m)\n
    w is size of machine word\n
    m is size of hash code you want in bits\n
    aa is any odd integer that fits in to machine word\n
    bb is any integer less than 2^(w - m)
    """

    _range = None
    _type = None

    _prime = 29996224275833
    _a = None
    _b = None

    _w = 64
    _aa = None
    _bb = None
    _m = None
    _rrange = None

    _seed_range = 1 << 30
    _seed = None

    _string_prime = 101111111111
    _string_a = None

    def __init__(self, hash_range=None, hash_type=UniversalHashType.MD5, hash_str=None):
        if hash_str != None:
            self.loads(hash_str)
            return
        self._range = hash_range
        self._type = hash_type
        if self._type == UniversalHashType.MD5:
            self._seed = str(random.randint(0, self._seed_range))
            return
        if self._type == UniversalHashType.OriginalInt:
            self._a = random.randint(1, self._prime - 1)
            self._b = random.randint(0, self._prime - 1)
        if self._type == UniversalHashType.FastInt:
            self._m = 1
            self._rrange = 2
            while self._rrange < hash_range:
                self._m += 1
                self._rrange *= 2
            self._aa = random.getrandbits(self._w) | 1
            self._bb = random.getrandbits(self._w - self._m)
        self._string_a = random.randint(1, self._string_prime)

    def hash_value(self, hash_key):
        if self._type == UniversalHashType.MD5:
            return int(
                int(hashlib.md5((str(hash_key) + '-' + self._seed).encode('utf-8')).hexdigest(), 16) % self._range)

        if (type(hash_key) is int):
            key = hash_key
        elif (type(hash_key) is str):
            key = 0
            for c in hash_key:
                key = ((key * self._string_a) + ord(c)) % self._string_prime
        else:
            return None

        if self._type == UniversalHashType.OriginalInt:
            return int(((self._a * key + self._b) % self._prime) % self._range)
        if self._type == UniversalHashType.FastInt:
            return int(((self._aa * key + self._bb) >> (self._w - self._m)) % self._range)

    def dumps(self):
        if self._type == UniversalHashType.MD5:
            return str(self._range) + '&' + str(self._type) + '&' + self._seed
        ret = str(self._range) + '&' + str(self._type) + '&' + str(self._string_a)
        if self._type == UniversalHashType.OriginalInt:
            return ret + '&' + str(self._a) + '&' + str(self._b)
        if self._type == UniversalHashType.FastInt:
            return ret + '&' + str(self._aa) + '&' + str(self._bb) + '&' + str(self._m) + '&' + str(self._rrange)
        return None

    def loads(self, hash_str):
        coeff = hash_str.split('&')
        self._range = int(coeff[0])
        self._type = int(coeff[1])
        if self._type == UniversalHashType.OriginalInt:
            self._string_a = int(coeff[2])
            self._a = int(coeff[3])
            self._b = int(coeff[4])
        if self._type == UniversalHashType.FastInt:
            self._string_a = int(coeff[2])
            self._aa = int(coeff[3])
            self._bb = int(coeff[4])
            self._m = int(coeff[5])
            self._rrange = int(coeff[6])
        if self._type == UniversalHashType.MD5:
            self._seed = coeff[2]


class LDPOracle(object):
    _eps = 1.0
    _exp = None
    _serialized = True

    def __init__(self, eps, serialize_data=True):
        self._eps = eps
        self._exp = math.exp(eps)
        self._serialized = serialize_data

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


class LDPNumRF(LDPOracle):

    def __init__(self, eps):
        super(LDPNumRF, self).__init__(eps)

    def encodes(self, value, **kwargs):
        min_val = kwargs["min_val"]
        max_val = kwargs["max_val"]

        value = float(value)

        if (random.random() < (value * 1.0 - min_val) / (max_val - min_val)) ^ (random.random() < 1 / (self._exp + 1)):
            ret = max_val
        else:
            ret = min_val

        return str(((self._exp + 1) * ret - (max_val + min_val)) / (self._exp - 1))

    def decodes(self, report, **kwargs):
        return float(report)