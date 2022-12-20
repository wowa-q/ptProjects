# pylint: skip-file
import pytest
import pathlib
import shutil
import random
import hashlib
import time
import os
from datetime import datetime

# user packages
from .context import dkb
from dkb.db import db_api as db
from dkb.dkb import Dkb
import dkb.api

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"
# PRODUCTIVE_CSV_DIR = pathlib.Path(__file__).parent.parent.resolve() / "dkb_p" / "csv"

@pytest.fixture
def db_file2copy():
    return FIXTURE_DIR / "db2test_copy.db"

@pytest.fixture
def db4test_handler():
    db_file2copy = FIXTURE_DIR / "db2test_copy.db"
    db_file = FIXTURE_DIR / "db4test.db"
    db_handler = db.DbHandler(db_file)
    yield db_handler
    db_handler.close()
    time.sleep(2)
    db_file.unlink()
    shutil.copy(db_file2copy, db_file)

@pytest.fixture
def meta_dict():
    ln_dict = {}
    ln_dict['date'] = datetime.now()
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['konto'] = 'yearly'
    ln_dict['checksum'] = random.randint(100000, 1000000)
    return ln_dict

@pytest.fixture
def archive():    
    csv_file = FIXTURE_DIR / 'move_temp.csv'
    shutil.copy(FIXTURE_DIR / 'move.csv', csv_file)
    zip_file = FIXTURE_DIR / 'archive.zip'
    yield zip_file, csv_file
    zip_file.unlink()

# ----------------------------------------------------------------
# ------------------ CSV Import tests  ---------------------------
# ----------------------------------------------------------------
@pytest.mark.run(order=1)
def test_import_csv(db4test_handler):
    '''
    - import the valid csv
    - new meta data entry was created

    '''
    db_handler = db4test_handler
    dkb_ld = Dkb()
    cmd = dkb.api.CmdImportNewCsv(db_handler, dkb_ld, FIXTURE_DIR / 'test1.csv')
    cmd.execute()
    
    with open(str(FIXTURE_DIR / 'test1.csv'), 'rb') as file:
        # calculate first the checksum of the given csv file
        checksum =  hashlib.md5(file.read()).hexdigest().upper()
    result = db_handler.find_checksum('123456789')
    assert len(result[1]) == 0, "Checksum could unexpectedly be found"
    result = db_handler.find_checksum(checksum)    
    assert len(result[1]) == 1, f"Checksum could not be found \
                                checksum: {checksum}"
    result = db_handler.get_month('2016', '06') 
    
    assert len(result[1]) == 7, f"Number of imported items is {len(result[1])} \
                                imported from {FIXTURE_DIR} \
                                entries: {result[1]}"
    # import the same csv again - no changes on db are made
    cmd.set_new_csv(FIXTURE_DIR / 'test1.csv')
    cmd.execute()
    result = db_handler.find_checksum(checksum)    
    assert len(result[1]) == 1, f"Checksum could not be found \
                                checksum: {checksum}"
    result = db_handler.get_month('2016', '06') 
    
    assert len(result[1]) == 7, f"Number of imported items is {len(result[1])} \
                                imported from {FIXTURE_DIR} \
                                entries: {result[1]}"
    # import test2.csv csv again - no changes on db are made
    cmd.set_new_csv(FIXTURE_DIR / 'test2.csv')
    cmd.execute()
    with open(str(FIXTURE_DIR / 'test2.csv'), 'rb') as file:
        # calculate first the checksum of the given csv file
        checksum =  hashlib.md5(file.read()).hexdigest().upper()
    result = db_handler.find_checksum(checksum)    
    assert len(result[1]) == 1, f"Checksum could not be found \
                                checksum: {checksum}"
    result = db_handler.get_month('2016', '06') 
    
    assert len(result[1]) == 9, f"Number of imported items is {len(result[1])} \
                                imported from {FIXTURE_DIR} \
                                entries: {result[1]}"

def test_csv_moved(archive):
    zip_file, csv_file = archive
    cmd_archive = dkb.api.CmdArchiveCsv(csv_file, zip_file)
    cmd_archive.execute()
    print('ASSERTIOINS START')
    # check new archive was created
    assert os.path.isfile(zip_file) == True, f"zip file wasn't created"
    # check csv file was deleted, after beeing archived
    assert os.path.isfile(csv_file) == False, f"File wasn't moved"
    

   



# @pytest.mark.datafiles( CSV_DIR / 'test1.csv',
#                         CSV_DIR / 'test2.csv',
#                         CSV_DIR / 'test3.csv',
#                         CSV_DIR / 'test4.csv',
#     )
# @pytest.mark.datafiles( CSV_DIR / 'test1.csv')
# plugin can be used to not modify the original file https://pypi.org/project/pytest-datafiles/
# @pytest.mark.datafiles(pathlib.Path(__file__).parent.resolve() / "fixtures" / "tst1.csv")
# def test_csv_read(pathes):
#     loader = dkb.Dkb() 
#     assert loader is not None
#     df, checksum = loader.get_dkb_df(pathes / 'tst.csv') # not utf-8 encoded
#     assert df is not None
#     assert len(checksum) != 0
#     dic = loader.get_meta(pathes / 'tst.csv')
#     assert dic["Kontonummer"] != ""
    '''
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfc in position 226: invalid start byte
    df, checksums = loader.get_dkb_df_from_folder(pathes) 
    assert len(loader.csv_files) > 0
    assert df is not None
    assert len(checksums) > 0
    assert len(checksums[0]) != 0
    '''
'''
def test_orm_import_in_db(pathes):
    loader = dkb.Dkb()
    csv_df = loader.get_dkb_df(pathes / 'tst.csv')
    o = orm.DbHandler(pathes, 'new_db_from_test', 'sqlite3')
    o.import_dkb_df(csv_df)
    # assert o != None
    # o.importDKBDF(csv_df)

# TODO: 
# FAILING when table already exists
# FAILING when connection to DB created without creating the table (they exist already)
def test_orm_create_tables(pathes):
    o = orm.DB_Handler(pathes, 'new_db_from_test', 'sqlite3')
    assert o != None
    o.create_cath_table()
    o.create_class_table()
    assert o._check_column_exists('Class') == False
    o.add_class_column()
    o.add_cath_column()
    cath_table = ['Versicherung', 4]
    class_data = ['out', 'bla', 'fix', 'lastschrift']
    o.add_new_cath(cath_table)
    o.add_new_class(class_data)
    o.add_new_cath(cath_table)
    o.add_new_class(class_data)

# FAILING - check the selector
def test_orm_get_db_data(pathes):
    o = orm.DbHandler(pathes, 'db4test', 'sqlite3')
    # data = o.get_month('2016', '04')
    # assert len(data) > 0
    o.update_engine()
    data = o.get_class()
    assert len(data) > 0
    assert data[0] == 'test1'

def test_db_connection(pathes):
    db = sq.DB(pathes, 'test_db', 'sqlite3')
    assert db != None
    check = db._createConnection()
    assert check == True
    db_file = Path(pathes / 'test_db.db')
    assert db_file.is_file() == True
    
def test_dbTableCreate(pathes):
    db = sq.DB(pathes, 'test_db', 'sqlite3')
    check = db._createConnection()
    db.createNewTable('category')

def test_dbImportDF(pathes):
    db = sq.DB(pathes, 'test_db', 'sqlite3')
    db.setTableName("dkb")
    loader = dkb.Dkb(pathes)
    df=loader.parseDkbData()

    # assert db.importNewData(df) == True

'''