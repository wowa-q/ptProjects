from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
# user packages:
from dkb.db.constructor import Base
from dkb.db.class_table import Classes_Table_Handler
from dkb.db.category_table import Category_Table_Handler
from dkb.db.meta_table import CSV_Table_Handler
from dkb.db.dkb_table import DKB_Table_Handler


class DB_Handler(object):
    def __init__(self, pth):
        print(pth)     
        self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        self.dkb_session = sessionmaker(bind=self.dkb_engine)        
    
    def close(self): # tested trows warning
        # self.dkb_session.close_all_sessions()
        self.dkb_session.close_all() # depricated - trows a warning

    def create_db(self, pth):   # tested     
        self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        self.dkb_session = sessionmaker(bind=self.dkb_engine)
        Base.metadata.create_all(self.dkb_engine)

    def create_classes(self, ln_dict): # tested
        table_handler = Classes_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)
    
    def create_category(self, ln_dict): # tested
        table_handler = Category_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)

    def create_csv_meta(self, ln_dict):
        table_handler = CSV_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)
    
    def create_dkb_table(self, ln_dict):
        table_handler = DKB_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)
    
    def import_dkb_df(self, csv_df, csv_meta):
        table_handler = DKB_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.import_csv_df(csv_df, csv_meta)

    def import_dkb_csv(self, csv_ln, csv_meta):
        table_handler = DKB_Table_Handler(self.dkb_session, self.dkb_engine)
        table_handler.import_pure_csv(csv_ln, csv_meta)

    def find_checksum(self, checksum): # tested
        table_handler = CSV_Table_Handler(self.dkb_session, self.dkb_engine)
        return table_handler.find_checksum(checksum)

    def get_month(self, year, month):
        table_handler = DKB_Table_Handler(self.dkb_session, self.dkb_engine)
        self.close()
        return table_handler.get_month(year, month)

    def get_class_from_classes_by_name(self, name): # tested
        table_handler = Classes_Table_Handler(self.dkb_session, self.dkb_engine)
        return table_handler.get_class_by_name(name)

    def get_cat_from_category_by_name(self, name): # tested
        table_handler = Category_Table_Handler(self.dkb_session, self.dkb_engine)
        return table_handler.get_category_by_name(name)

    