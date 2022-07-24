from federatedscope.db.processor.basic_processor import BasicSQLProcessor


class GeneralProcessor(BasicSQLProcessor):
    def check(self):
        pass

    # TODO: @xuchen
    def execute(self, query, table):
        """Execute query based on the database

        Args:
            query:

        Returns:

        """
        pass
