from sqlalchemy import Column, String, Integer
from dkb.db.constructor import Base

class Category(Base):
    __tablename__ = "category"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    type = Column("type", String)    
    cycle = Column("cycle", String)

    def __init__(self, name, type, cycle) -> None:
        self.name = name
        self.type = type        
        self.cycle = cycle

    def __repr__(self) -> str:
        return f"category: {self.name}"

class Category_Table_Handler(object):

    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine

    def add(self, ln_as_dict):
        name=ln_as_dict['name']
        type=ln_as_dict['type']
        cycle=ln_as_dict['cycle']
        new_category = Category(name, type, cycle)
        self.session.add(new_category)
        self.session.commit()

    def get_category_by_name(self, category):
        result = self.session.query(Category.name, 
                                    Category.type, 
                                    Category.cycle
                                    ).filter(Category.name == category).first() 
        return result
    
    def update_category(self, category, **value):
        to_update = self.session.query(Category).filter(Category.name == category).first()
        if value.haskey('type'):
            to_update.type = value['type']
        if value.haskey('cycle'):
            to_update.cycle = value['cycle']
        