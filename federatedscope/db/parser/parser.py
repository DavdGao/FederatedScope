from federatedscope.db.model.sqlquery import SQLQuery

class SQLParser(object):

    def parse(self, statement):
        """Parse the statement into SQL query

        Args:
            statement:

        Returns:

        """
        return SQLQuery(statement)

    def check_syntax(self, statement):
        """Check the syntax of the statement

        Args:
            cmd:

        Returns:

        """
        return True