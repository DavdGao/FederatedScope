from federatedscope.db.model.sqlquery_pb2 import BasicSchedule
from federatedscope.db.enums import KEYWORDS, COMPARE_OPERATORS, AGGREGATE_OPERATORS
import federatedscope.db.model.sqlquery_pb2 as querypb
import federatedscope.db.model.data_pb2 as datapb
from federatedscope.db.model.sqlschedule import Query

import re


class Statement(object):
    def __init__(self, statement: str):
        self.index = 0
        self.statement = self.init_statement(statement)

    def init_statement(self, statement: str):
        # TODO: imporve to suit a more complex grammar, not support ['<', '>'] yet
        for operator in ['>=', '<=']:
            statement = statement.replace(operator, f' {operator} ')
        statement = re.sub(r'[<>]([^=])', r' < \1', statement)
        statement = re.sub(r'([^<>])=', r'\1 = ', statement)
        return [
            ele for ele in statement.replace('(', ' ').replace(
                ')', ' ').strip().split(' ') if ele
        ]

    def __len__(self):
        return len(self.statement)

    def get_last(self):
        return self.statement[self.index - 1]

    def get_word(self, index=None, delta=0):
        if index is None:
            index = self.index
        try:
            return self.statement[index + delta]
        except IndexError:
            return None

    def get_next(self):
        return self.statement[self.index + 1]

    def step(self):
        self.index += 1
        return self.statement[self.index - 1]

    def isFinish(self):
        return self.index >= len(self.statement)

    def isDigit(self, index=None):
        if index is None:
            index = self.index
        return self.statement[index].isdigit()


class SQLParser(object):
    KEYWORDS = [
        'SELECT', 'ALL', 'DISTINCT'
        'FROM', 'WHERE', 'GROUPBY', 'COUNT', 'AVG'
        'SUM', 'JOIN'
    ]

    COMPARE_OPERATORS = ['=', '>', '>=', '<', '<=']

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
        while not statement.isFinish():
            word = statement.step()
            if word.upper() == KEYWORDS.SELECT:
                # Handle multi aggregate exps
                while statement.get_word().upper() in AGGREGATE_OPERATORS:
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
            elif word.upper() == KEYWORDS.FROM:
                query.table_name = statement.step()
            elif word.upper() == KEYWORDS.WHERE:
                # Handle multi boolean exps
                # TODO: split expression into several exps
                # NOTE: only support <reference> <operator> <literal> pattern
                while statement.get_word(
                        delta=1) in COMPARE_OPERATORS.values():
                    # TODO: suppose they are all triples
                    left_attr = statement.step()
                    operator = statement.step()
                    right_attr = statement.step()

                    exp_bool = query.exp_where.add()
                    exp_bool.operator = getattr(
                        querypb.Operator, COMPARE_OPERATORS.get_key(operator))

                    attr = exp_bool.children.add()
                    attr.operator = querypb.Operator.REF
                    attr.s = left_attr

                    attr = exp_bool.children.add()
                    attr.operator = querypb.Operator.LIT
                    try:
                        attr.i = int(right_attr)
                        attr.type = datapb.DataType.INT
                    except ValueError:
                        try:
                            attr.f = float(right_attr)
                            attr.type = datapb.DataType.FLOAT
                        except ValueError:
                            attr.type = datapb.DataType.STRING
                            attr.s = right_attr.strip("'")
                    if not statement.isFinish():
                        statement.step()  # skip AND
            else:
                raise RuntimeError(f"{statement.get_next()} not support.")
        print(str(query))
        return Query(query)

    def check_syntax(self, statement):
        """Check the syntax of the statement

        Args:
            cmd:

        Returns:

        """
        # TODO: with the help of sqlparser
        return True
