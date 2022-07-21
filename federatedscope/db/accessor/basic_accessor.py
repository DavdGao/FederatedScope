from abc import abstractmethod
from abc import ABC


class BasicAccessor(ABC):
    """Accessor is used to connect DBMS and processor, the operations called by the processor will be translated into the standard operations of the corresponding DBMS

    """
    def __init__(self, root):
        self.root = root

    @abstractmethod
    def connect(self):
        """Connect accessor based on the fundamental DBMS

        Note:
            for csv accessor, we directly load it into the memory and process it with pandas, while for others, the processing is up to the specific DBMS

        Returns:

        """
        pass

    @abstractmethod
    def get_table(self, table_name=None):
        pass

    @abstractmethod
    def get_schema(self):
        """Return a wrapped schema in the format of proto buffers

        Returns:
            wrapped schema (pb)

        """
        pass

    @abstractmethod
    def join(self):
        """Execute join in the corresponding DBMS

        Returns:

        """
        pass

    @abstractmethod
    def query(self, query):
        """Execute query in the corresponding DBMS

        Returns:

        """

    @abstractmethod
    def write_table(self, table):
        pass
