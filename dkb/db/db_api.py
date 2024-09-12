''' contains APIs to be used to interact with the data base '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# user packages:
from dkb.db.constructor import Base
from dkb.db.class_table import ClassesTableHandler
from dkb.db.category_table import CategoryTableHandler
from dkb.db.meta_table import CsvMetaTableHandler
from dkb.db.dkb_table import DkbTableHandler

# pylint: disable=too-few-public-methods
class DbHandler():
    ''' wrapper to all table interfaces '''
    def __init__(self, pth):
        print(pth)     
        self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        self.dkb_session = sessionmaker(bind=self.dkb_engine)        
    
    def close(self): # tested trows warning
        ''' to close the session'''
        # self.dkb_session.close_all_sessions()
        self.dkb_session.close_all() # depricated - trows a warning

    def create_db(self, pth):   # tested
        ''' API to create new data base '''  
        self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        self.dkb_session = sessionmaker(bind=self.dkb_engine)
        Base.metadata.create_all(self.dkb_engine)

    def create_classes(self, ln_dict): # tested
        ''' API to create Classes table '''
        table_handler = ClassesTableHandler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)
    
    def create_category(self, ln_dict): # tested
        ''' API to create Category table '''
        table_handler = CategoryTableHandler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)

    def create_csv_meta(self, ln_dict):
        ''' API to create csv-meta table '''
        table_handler = CsvMetaTableHandler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)
    
    def create_dkb_table(self, ln_dict):
        ''' API to create dkb-table table '''
        table_handler = DkbTableHandler(self.dkb_session, self.dkb_engine)
        table_handler.add(ln_dict)

    def import_dkb_csv(self, csv_ln, csv_meta):
        ''' API to csv file into data base '''
        table_handler = DkbTableHandler(self.dkb_session, self.dkb_engine)
        table_handler.import_pure_csv(csv_ln, csv_meta)

    def find_checksum(self, checksum): # tested
        ''' API to check/find a checksum in the dkb-table '''
        table_handler = CsvMetaTableHandler(self.dkb_session, self.dkb_engine)
        return table_handler.find_checksum(checksum)

    def get_month(self, year, month):
        ''' API to retrive month data from the data base '''
        table_handler = DkbTableHandler(self.dkb_session, self.dkb_engine)
        self.close()
        return table_handler.get_month(year, month)

    def get_class_from_classes_by_name(self, name): # tested
        ''' API to retrive Classes from the table '''
        table_handler = ClassesTableHandler(self.dkb_session, self.dkb_engine)
        return table_handler.get_class_by_name(name)

    def get_cat_from_category_by_name(self, name): # tested
        ''' API to retrive Category from the table '''
        table_handler = CategoryTableHandler(self.dkb_session, self.dkb_engine)
        return table_handler.get_row_by_name(name)
    