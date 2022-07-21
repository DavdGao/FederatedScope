class KEYWORDS:
    SELECT = 'SELECT'
    FROM = 'FROM'
    WHERE = 'WHERE'
    GROUPBY = 'GROUPBY'


from enum import Enum, EnumMeta


class StrEnumMeta(EnumMeta):
    def __contains__(cls, member):
        if isinstance(member, Enum):
            return isinstance(member,
                              cls) and member._name_ in cls._member_map_
        elif isinstance(member, str):
            return member in cls._member_map_
        else:
            raise TypeError(
                "unsupported operand type(s) for 'in': '%s' and '%s'" %
                (type(member).__qualname__, cls.__class__.__qualname__))

    def keys(cls):
        return cls._member_names_

    def values(cls):
        return list(cls._value2member_map_.keys())


class AGGREGATE_OPERATORS(Enum, metaclass=StrEnumMeta):
    SUM = 'SUM'
    COUNT = 'COUNT'
    AVG = 'AVG'


class COMPARE_OPERATORS(Enum, metaclass=StrEnumMeta):
    EQ = '='
    GT = '>'
    LT = '<'
    GE = '>='
    LE = '<='

    @classmethod
    def get_key(cls, op):
        return cls._value2member_map_[op].name
