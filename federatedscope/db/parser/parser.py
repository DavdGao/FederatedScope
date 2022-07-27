from ast import keyword
from federatedscope.db.model.sqlquery_pb2 import BasicSchedule
from federatedscope.db.enums import COMPARE_OPERATORS
import federatedscope.db.model.sqlquery_pb2 as querypb
from federatedscope.db.model.sqlschedule import Query

import re
import sqlparse
from sqlparse.sql import Function, Comparison, Where, Identifier
from sqlparse.tokens import Token

class SQLParser(object):

    def __init__(self):
        self.CMP_REVERSE = { '=' : '=',
                        '>': '<',
                        '>=': '<=',
                        '<' : '>',
                        '<=' :'>='
                    }

    def parse_literal(self, lit_token, lit_exp):
        lit_exp.operator = querypb.Operator.LIT
        if lit_token.ttype == Token.Literal.Number.Integer:
            lit_exp.i = int(lit_token.value)
        elif lit_token.ttype == Token.Literal.Number.Float:
            lit_exp.f = float(lit_token.value)
        elif lit_token.ttype == Token.Literal.String.Single:
            lit_exp.s = lit_token.value.strip("'")
        else:
            raise ValueError("Unsupported literal type: ", str(lit_token))

    def parse_func(self, func_token, func_exp):
        params = func_token.get_parameters()
        func_name = func_token.tokens[0].value
        func_exp.operator = getattr(querypb.Operator, func_name.upper())
        for para in params:
            child = func_exp.children.add()
            if isinstance(para, Identifier):
                child.operator = querypb.Operator.REF
                child.s = para.value
            else:
                self.parse_literal(para, child)

    def parse_cmp(self, cmp, cmp_exp):
        left = cmp_exp.children.add()
        right = cmp_exp.children.add()
        left_token = cmp.left
        right_token = cmp.right
        op = cmp.tokens[2].value
        # reverse if identifier is at right
        if isinstance(cmp.right, Identifier) and not isinstance(cmp.left, Identifier):
            left_token = cmp.right
            right_token = cmp.left
            op = self.CMP_REVERSE[op]
        left.operator = querypb.Operator.REF
        left.s = left_token.value
        self.parse_literal(right_token, right)
        cmp_exp.operator = getattr(
                    querypb.Operator, COMPARE_OPERATORS.get_key(op))

    def parse_where(self, where_tokens):
        where_exps = []
        for token in where_tokens[2:]:
            if token.is_whitespace:
                continue
            elif isinstance(token, Comparison):
                filt = querypb.Expression()
                self.parse_cmp(token, filt)
                where_exps.append(filt)
            elif token.value.lower() == 'and':
                continue
            else:
                raise ValueError("unsupported operation in where clause: " + str(token.value))
        return where_exps

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
        tokens = sqlparse.parse(statement_str)
        if len(tokens) == 0:
            return
        elif len(tokens[0].tokens) == 0:
            return
        elif tokens[0].tokens[0].normalized != 'SELECT':
            raise ValueError("Unsupported query: " + statement_str)
        tokens = tokens[0].tokens
        query = BasicSchedule()
        out_tokens = []
        idx = 0
        from_idx = 0
        for token in tokens[1:]:
            idx += 1
            if token.is_whitespace:
                continue
            elif token.is_keyword and token.normalized == 'FROM':
                from_idx = idx
                break
            else:
                out_tokens.append(token)

        if len(tokens) <= from_idx + 2 or not isinstance(tokens[from_idx + 2], Identifier):
            raise ValueError("Source table not found in FROM clause")
        else:
            query.table_name = tokens[from_idx + 2].value

        for token in out_tokens:
            if isinstance(token, Function):
                agg = query.exp_agg.add()
                self.parse_func(token, agg)
            elif isinstance(token, Identifier):
                sel = query.exp_select.add()
                sel.operator = querypb.Operator.REF
                sel.s = token.value
            else:
                raise ValueError("Unsupported operation in select clause")

        for token in tokens[from_idx + 3:]:
            if token.is_whitespace:
                continue
            elif isinstance(token, Where):
                where_exps = self.parse_where(token)
                query.exp_where.extend(where_exps)
            else:
                raise ValueError("Unsupported clause " + str(token))
        return Query(query)

    def check_syntax(self, statement):
        """Check the syntax of the statement

        Args:
            cmd:

        Returns:

        """
        # TODO: with the help of sqlparser
        return True
