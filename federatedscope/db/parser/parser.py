from federatedscope.db.model.sqlquery_pb2 import BasicQuery

class SQLParser(object):
    KEYWORDS = [
        'select',
        'all',
        'distinct'
        'from',
        'where',
        'groupby',
        'count',
        'avg',
        'mean'
        'join'
    ]
    def parse(self, statement: str):
        """Parse the statement into SQL query

        Args:
            statement:

        Returns:

        """

        query = BasicQuery()
        # For now, we don't consider the nested query
        # TODO: nested query
        # TODO: consider the whitespace after ','
        words = statement.strip().split(' ')
        i = 0
        while i < len(words):
            # Current word
            word = words[i]
            next_word = words[i+1]

            if word.upper() == 'SELECT':
                query.exp_select = next_word
            elif word.upper() == 'FROM':
                query.exp_from = next_word
            elif word.upper() == 'WHERE':
                query.exp_where = next_word
            elif word.upper() == 'GROUPBY':
                query.exp_groupby = next_word
            # elif word.upper() == 'HAVING':
            #     query.exp_have = next_word
            # elif word.upper() == 'ORDERBY':
            #     query.exp_orderby = next_word
            # elif word.upper() == 'LIMIT':
            #     query.exp_limit = next_word

        return query


    def check_syntax(self, statement):
        """Check the syntax of the statement

        Args:
            cmd:

        Returns:

        """
        return True