from federatedscope.db.model.sqlquery_pb2 import BasicSchedule
from federatedscope.db.enums import KEYWORDS, COMPARE_OPERATORS, AGGREGATE_OPERATORS
import federatedscope.db.model.sqlquery_pb2 as querypb

class Statement(object):
    def __init__(self, statement: str):
        self.index = 0
        self.statement = statement.strip().split(' ')

    def __len__(self):
        return len(self.statement)

    def get_last(self):
        return self.statement[self.index-1]

    def get_word(self, index=None, delta=0):
        if index is None:
            index = self.index
        try:
            return self.statement[index+delta]
        except IndexError:
            return None

    def get_next(self):
        return self.statement[self.index+1]

    def step(self):
        self.index += 1
        return self.statement[self.index]

    def isFinish(self):
        return self.index == len(self.statement)-1

    def isDigit(self, index=None):
        if index is None:
            index = self.index
        return self.statement[index].isdigit()

class SQLParser(object):
    KEYWORDS = [
        'SELECT',
        'ALL',
        'DISTINCT'
        'FROM',
        'WHERE',
        'GROUPBY',
        'COUNT',
        'AVG'
        'SUM',
        'JOIN'
    ]

    COMPARE_OPERATORS = [
        '=',
        '>',
        '>=',
        '<',
        '<='
    ]


    def parse(self, statement_str: str):
        """Parse the statement into SQL query

        select:
            SELECT [ STREAM ] [ ALL | DISTINCT ]
              { * | projectItem [, projectItem ]* }
            FROM tableExpression
            [ WHERE booleanExpression ]
            [ GROUP BY { groupItem [, groupItem ]* } ]

        Args:
            statement:

        Returns:

        """

        query = BasicSchedule()
        statement = Statement(statement_str)
        while statement.isFinish():
            word = statement.step()
            if word == KEYWORDS.SELECT:
                # Handle multi aggregate exps
                while statement.get_next() in AGGREGATE_OPERATORS:
                    # Aggregated expression
                    word = statement.step()
                    # Build aggregation exp
                    agg = query.exp_agg.add()
                    agg.operator = getattr(querypb.Operator, word.upper())
                    agg_attr = agg.children.add()
                    agg_attr.operator = querypb.Operator.REF
                    # Obtain attribute
                    attribute = statement.step()
                    agg_attr.s = attribute
            elif word == KEYWORDS.FROM:
                query.table_name = statement.step()
            elif word == KEYWORDS.WHERE:
                # Handle multi boolean exps
                while statement.get_word(delta=2) in COMPARE_OPERATORS:
                    # TODO: suppose they are all triples
                    left_attr = statement.step()
                    left_lit = statement.isDigit()
                    operator = statement.step()
                    right_attr = statement.step()
                    right_lit = statement.isDigit()

                    exp_bool = query.exp_where.add()
                    exp_bool.operator = getattr(querypb.Operator, COMPARE_OPERATORS.get_str(operator))

                    attr = exp_bool.children.add()
                    attr.operator = querypb.Operator.LIT if left_lit else querypb.Operator.REF
                    attr.s = left_attr

                    attr = exp_bool.children.add()
                    attr.operator = querypb.Operator.REF if right_lit else querypb.Operator.REF
                    attr.s = right_attr
            else:
                raise RuntimeError(f"{statement.get_next()} not support.")

        return query


    def check_syntax(self, statement):
        """Check the syntax of the statement

        Args:
            cmd:

        Returns:

        """
        return True