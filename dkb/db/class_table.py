'''
Interface to db table Classes
'''

from sqlalchemy import Column, String, Integer
#from sqlalchemy import ForeignKey, CHAR
from dkb.db.constructor import Base

# pylint: disable=too-few-public-methods
class Classes(Base):
    ''' class to build a table in the data base '''
    __tablename__ = "classes"
    id = Column("id", Integer, primary_key=True)
    inout = Column("inout", String)
    name = Column("name", String, unique=True)
    fix = Column("fix", String)

    def __init__(self, name, inout, fix) -> None:
        self.name = name
        self.inout = inout
        self.fix = fix

    def __repr__(self) -> str:
        return f"Class: {self.name}"

class ClassesTableHandler():
    ''' class providing methods to work with the table from data base '''
    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine
    
    def add(self, ln_as_dict):
        ''' method to add new entry in the table '''
        new_class = Classes(inout =ln_as_dict['inout'],
                            name=ln_as_dict['name'],
                            fix=ln_as_dict['fix'])
        self.session.add(new_class)
        self.session.commit()

    def get_class_by_name(self, dkb_class):
        ''' use filter class name to retrive data from the table '''
        result = self.session.query(Classes.name,
                                    Classes.inout,
                                    Classes.fix,
                                    Classes.id
                                    ).filter(Classes.name == dkb_class).first() 
        return result
    
    def update_class(self, dkb_class, **value):
        ''' method to update the class in the table '''
        to_update = self.session.query(Classes).filter(Classes.name == dkb_class).first()
        if 'fix' in value:
            to_update.fix = value['fix']
        if 'inou' in value:
            to_update.inout = value['inout']
