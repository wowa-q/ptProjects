from sqlalchemy import ForeignKey, Column, String, Integer, CHAR
from dkb.db.constructor import Base


class Classes(Base):
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

class Classes_Table_Handler(object):

    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine
    
    def add(self, ln_as_dict):
        new_class = Classes(inout =ln_as_dict['inout'],
                            name=ln_as_dict['name'],
                            fix=ln_as_dict['fix'])
        self.session.add(new_class)
        self.session.commit()

    def get_class_by_name(self, dkb_class):
        result = self.session.query(Classes.name,
                                    Classes.inout,
                                    Classes.fix,
                                    Classes.id
                                    ).filter(Classes.name == dkb_class).first() 
        return result
    
    def update_class(self, dkb_class, **value):
        to_update = self.session.query(Classes).filter(Classes.name == dkb_class).first()
        if value.haskey('fix'):
            to_update.fix = value['fix']
        if value.haskey('inout'):
            to_update.inout = value['inout']
        