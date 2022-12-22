'''
Interface to db table Category
'''
import deprecation

from sqlalchemy import Column, String, Integer
from dkb.db.constructor import Base
from dkb.db import constructor as con
#from dkb.db.constructor import TableHandler


# pylint: disable=too-few-public-methods
class Category(Base):
    ''' class to build a table in the data base '''
    __tablename__ = "category"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    type = Column("type", String)    
    cycle = Column("cycle", String)

    def __init__(self, name, mtype, cycle) -> None:
        self.name = name
        self.type = mtype        
        self.cycle = cycle

    def __repr__(self) -> str:
        return f"category: {self.name}"

class CategoryTableHandler(con.TableHandler):
    ''' class providing methods to work with the table from data base '''
    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine

    def add(self, ln_as_dict):
        ''' method to add new entry in the table '''
        name=ln_as_dict['name']
        mtype=ln_as_dict['type']
        cycle=ln_as_dict['cycle']
        new_category = Category(name, mtype, cycle)
        self.session.add(new_category)
        self.session.commit()

    @deprecation.deprecated(details="Use get_row_by_name(name) instead")
    def get_category_by_name(self, category):
        ''' use filter category name to retrive data from the table '''
        result = self.session.query(Category.name, 
                                    Category.type, 
                                    Category.cycle
                                    ).filter(Category.name == category).first() 
        return result
    
    def get_row_by_name(self, name):
        """to get a row by name
        
        Args:
            name (String): column name
        """
        result = self.session.query(Category.name, 
                                    Category.type, 
                                    Category.cycle
                                    ).filter(Category.name == name).first() 
        return result

    @deprecation.deprecated(details="Use update_row(name, **values) instead")
    def update_category(self, category, **value):
        ''' method to update the category in the table '''
        to_update = self.session.query(Category).filter(Category.name == category).first()
        if 'type' in value:
            to_update.type = value['type']
        if 'cycle' in value:
            to_update.cycle = value['cycle']
    
    def update_row(self, name, **values):
        """to update the row, filtered by name

        Args:
            name (String): column name
            **values (Dict): positional arguments type, cycle
        """
        to_update = self.session.query(Category).filter(Category.name == name).first()
        
        if 'type' in values:
            to_update.type = values['type']
        if 'cycle' in values:
            to_update.cycle = values['cycle']

    def get_table_length(self) -> int:
        """returns the number of lines of the catogory table

        Returns:
            int: number of lines
        """
        return 0
