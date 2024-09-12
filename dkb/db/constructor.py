''' The module is required to be imported to have 
a use of the same Base instance '''
from abc import ABC, ABCMeta, abstractmethod

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker()


class DbConstructor(): # pylint: disable=too-few-public-methods
    ''' class to provide instances of Base and Session'''
    def __init__(self):
        # pylint: disable=invalid-name
        self.Base = declarative_base()
        self.Session = sessionmaker()
        # self.Session.close_all()
        # self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        # self.dkb_session = sessionmaker(bind=self.dkb_engine)
        
class TableHandler(ABC):
    """Master class to be used by all Table Handlers
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_table_length(self) -> int:
        """returns the number of lines of the catogory table

        Returns:
            int: number of lines
        """

    # to run standard commands
    @abstractmethod
    def add(self, ln_as_dict) -> None:
        """to add an entry to the table

        Args:
            ln_as_dict (Dictionary): complete row as dictionary
        """
    
    @abstractmethod
    def get_row_by_name(self, name):
        """to get a row by name
        
        Args:
            name (String): column name
        """
    
    @abstractmethod
    def update_row(self, name, **values):
        """to update the row, filtered by name

        Args:
            name (String): column name
        """
    
    