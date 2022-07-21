import federatedscope.db.model.sqlquery_pb2 as querypb
import federatedscope.db.model.data_pb2 as datapb


class Query(object):
    def __init__(self, querypb):
        self.querypb = querypb

    def target_table_name(self):
        return self.querypb.table_name

    def get_simple_agg(self):
        """
        get simple aggregate exps in the query plan.
        a simple aggregate means the expression has only one aggregate function,
        and the aggregate function directly takes an attribtue as input 

        Returns:
            list of (attribute name, aggregate function)
        """
        agg_exps = self.querypb.exp_agg
        aggregates = []
        for exp in agg_exps:
            attr = exp.children[0].s
            aggregates.append((attr, exp.operator))
        return aggregates

    def get_range_predicate(self):
        """
        get range filters in predicate
        
        Returns:
            list of (attribute name, (min_value, max_value))
        """
        where_exps = self.querypb.exp_where
        filters = {}
        for exp in where_exps:
            children = exp.children
            if children[0].operator == querypb.Operator.REF and children[
                    1].operator == querypb.Operator.LIT:
                attr = children[0].s
                lit_type = children[1].type
                if lit_type == datapb.DataType.INT:
                    value = children[1].i
                elif lit_type == datapb.DataType.FLOAT:
                    value = children[1].f
                else:
                    value = children[1].s
            else:
                raise ValueError("Unsupported where exp")
            if exp.operator == querypb.Operator.GE:
                if attr not in filters:
                    filters[attr] = {}
                    filters[attr]['min'] = value
                elif 'min' not in filters[attr]:
                    filters[attr]['min'] = value
                else:
                    raise ValueError("Unsupported overlap range")
            elif exp.operator == querypb.Operator.LE:
                if attr not in filters:
                    filters[attr] = {}
                    filters[attr]['max'] = value
                elif 'max' not in filters[attr]:
                    filters[attr]['max'] = value
                else:
                    raise ValueError("Unsupported overlap range")
            elif exp.operator == querypb.Operator.EQ:
                if attr in filters:
                    raise ValueError("Unsupported overlap range")
                else:
                    filters[attr] = {}
                    filters[attr]['min'] = value
                    filters[attr]['max'] = value
        return filters
