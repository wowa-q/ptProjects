import pytest
import pathlib
import shutil
import time
from datetime import datetime
from unittest.mock import Mock
import random

# user packages
from .context import dkb
from dkb.db import db_api as db
# from dkb.db.constructor import Base
from dkb.db import dkb_table, class_table 
from dkb import dkb
from dkb import api

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"

@pytest.fixture
def db_file2create():
    db_file = FIXTURE_DIR / "test_db_created.db"
    yield db_file 
    # delete the modified db file and copy one to make repeat of the test possible
    try:
        db_file.unlink()
    except FileNotFoundError:
        pass

@pytest.fixture
def db_file2copy():
    return FIXTURE_DIR / "db2test_copy.db"

@pytest.fixture
def db_file2modify(db_file2copy):
    db_file = FIXTURE_DIR / "db4test.db"
    yield db_file 
    # delete the modified db file and copy one to make repeat of the test possible
    db_file.unlink()
    shutil.copy(db_file2copy, db_file)

@pytest.fixture
def db_file2test():
    return FIXTURE_DIR / "db2test.db"

@pytest.fixture
def classes_dict():
    ln_dict = {}
    ln_dict['inout'] = 'IN'
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['fix'] = 'TRUE'
    return ln_dict

@pytest.fixture
def cat_dict():
    ln_dict = {}
    ln_dict['type'] = 'Steuer'
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['cycle'] = 'yearly'
    return ln_dict

@pytest.fixture
def meta_dict():
    ln_dict = {}
    ln_dict['date'] = datetime.now()
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['konto'] = 'yearly'
    # ln_dict['checksum'] = '12345'
    ln_dict['checksum'] = random.randint(100000, 1000000)
    return ln_dict

@pytest.fixture
def dkb_line():
    ln = "27.06.2016;27.06.2016;GUTSCHRIFT;OLGA MERKEL;Dankee rest folgt;DE15410500950001708361;WELADED1HAM;190;;;NOTPROVIDED"

def teardown_db(db_file, db_file2copy):
    db_file.unlink() # to delete the file after it was created to be able to repeat the test
    shutil.copy(db_file2copy, db_file)


def test_db_created(db_file2create):
    # test: new db file with tables can be created  
    fileList=list(FIXTURE_DIR.glob('**/*.db'))
    before = len(fileList)
    db_handler = db.DB_Handler(FIXTURE_DIR)
    db_handler.create_db(db_file2create)
    fileList=list(FIXTURE_DIR.glob('**/*.db'))
    after = len(fileList)  
    assert before < after, "no new db was created"


def test_import_single_class(classes_dict, db_file2modify):
    #test: new class can be added
    db_handler = db.DB_Handler(db_file2modify)    
    db_handler.create_classes(classes_dict)
    result = db_handler.get_class_from_classes_by_name(classes_dict['name'])    
    db_handler.close()     
    assert result is not None, f"Class: {classes_dict['name']} in Classes Table couldn't be found "

def test_import_single_cat(cat_dict, db_file2modify): 
    # test: new category can be added
    db_handler = db.DB_Handler(db_file2modify)    
    db_handler.create_category(cat_dict)
    result = db_handler.get_cat_from_category_by_name(cat_dict['name'])    
    db_handler.close()
    assert result is not None, f"Class: {cat_dict['name']} in Category Table couldn't be found "

def test_create_new_single_meta(meta_dict, db_file2modify): 
    # test: new meta entry can be added 
    db_handler = db.DB_Handler(db_file2modify)    
    db_handler.create_csv_meta(meta_dict)
    result = db_handler.find_checksum(meta_dict['checksum'])    
    db_handler.close()     
    assert len(result[1]) > 0, f"Meta Entry: {meta_dict['checksum']} in Meta Table couldn't be found "


def test_import_test1_csv():
    '''
    to 
    import shutil
    shutil.move(src, dst)
    shutil.copy(src, dst)
    shutil.copytree(src, dst)
    '''
    pytest.skip('not correct test')
    db_file = pathes / "db4test.db"
    db_handler = db.DB_Handler(db_file)
    session = db_handler.dkb_session()
    before = len(session.query(dkb_table.DKB_Table.checksum).all())
    dkb_ld = dkb.DKB()
    csv_file = pathes / "test2.csv"
    importer = api.CmdImportNewCsv(db_handler, dkb_ld, csv_file)
    importer.execute()
    # dkb_handler = dkb_table.DKB_Table_Handler(db_handler.dkb_session, db_handler.dkb_engine)
    # engine = db_handler.dkb_engine
    result = session.query(dkb_table.DKB_Table.checksum).all()
    assert len(result) > before, f"result retrived, before: {before} after: {len(result)}"

# @pytest.mark.datafiles('/opt/big_files/film1.mp4')
# def test_fast_forward(datafiles):
#     path = str(datafiles)  # Convert from py.path object to path (str)
#     assert len(os.listdir(path)) == 1
#     assert os.path.isfile(os.path.join(path, 'film1.mp4'))
#     #assert some_operation(os.path.join(path, 'film1.mp4')) == expected_result

#     # Using py.path syntax
#     assert len(datafiles.listdir()) == 1
#     assert (datafiles / 'film1.mp4').check(file=1)

