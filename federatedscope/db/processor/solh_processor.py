from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.data_pb2 import Schema, DataType
from federatedscope.db.model.sqlquery_pb2 import Operator
from google.protobuf import text_format
from federatedscope.db.algorithm.ldp import LDPOLH

import numpy as np


class SOLHProcessor(BasicSQLProcessor):
    def __init__(self, epsilon):
        super(SOLHProcessor, self).__init__()
        self.eps = epsilon
        self.ldp = LDPOLH(epsilon)

    def check_agg(self, query):
        """
        check if the select clause contains only COUNT(*)

        Returns:
            list of (attribute name, aggregate function)
        """
        agg_exps = query.querypb.exp_agg
        if len(agg_exps) != 1 or agg_exps[0].operator != Operator.COUNT or len(agg_exps[0].children) != 0:
            raise ValueError("Only support COUNT(*) in SOLH")

    def get_predicate(self, query):
        """
        get predicate in where clause

        Returns:
            (attr_name, value)
        """
        where_exps = query.querypb.exp_where
        if len(where_exps) > 1:
            raise ValueError("SOLH only supports a single equivalent filter")
        for exp in where_exps:
            children = exp.children
            if children[0].operator == Operator.REF and children[
                    1].operator == Operator.LIT:
                attr = children[0].s
                lit_type = children[1].type
                if lit_type == DataType.INT:
                    value = children[1].i
                elif lit_type == DataType.FLOAT:
                    value = children[1].f
                else:
                    value = children[1].s
            else:
                raise ValueError("Only supports column compare with value")
            if exp.operator != Operator.EQ:
                raise ValueError("SOLH only supports = where clause")
        return (attr, value)

    def check(self, query):
        self.check_agg(query)
        self.get_predicate(query)


    def prepare(self, table):
        self.sensitive_attributes = table.schema.sensitive_attr_names()
        self.unsensitive_attributes = table.schema.unsensitive_attrs_names()

    def query(self, query, table):
        """
        solh query on table
        Args:
            query (Query): query plan
            table (Table): the table
        """

        (attr, value) = self.get_predicate(query)
        return self.ldp.decode_table(table, attr, value)
