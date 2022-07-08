
class KEYWORDS:
    SELECT = 'SELECT',
    FROM = 'FROM'
    WHERE = 'WHERE'
    GROUPBY = 'GROUPBY'


class AGGREGATE_OPERATORS:
    SUM = 'SUM'
    COUNT = 'COUNT'
    AVG = 'AVG'

    def __contains__(self, item):
        return item in [AGGREGATE_OPERATORS.SUM,
                        AGGREGATE_OPERATORS.COUNT,
                        AGGREGATE_OPERATORS.AVG]


class COMPARE_OPERATORS:
    OPS = { 
        'EQ': '=',
        'GE': '>',
        'LE': '<',
        'GEQ': '>=',
        'LEQ': '<='
    }
    
    def __getattr__(self, item):
        if item in COMPARE_OPERATORS.OPS:
            return COMPARE_OPERATORS[item]
        else:
            return super(COMPARE_OPERATORS, self).__getattr__(item)

    def __contains__(self, item):
        return item in COMPARE_OPERATORS.OPS.values()

    def get_str(self, op):
        keys, values = COMPARE_OPERATORS.OPS.items()
        return keys[list(values).index(op)]
