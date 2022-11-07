import pytest
from pathlib import Path

# user packages
import dkb.dkb as dkb
import dkb.db as sq
import fl.fileLoader as fl
import dkb.orm as orm



@pytest.fixture
def pathes():
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    return pth

def test_FileLoaderInitialization(pathes):
    # invalid path
    loader = fl.FileLoader('')
    assert loader.path != None
    fileList = loader.getCsvFilesList()
    assert fileList is not None
    assert len(fileList) == 0
    # folder with csv files 
    loader = fl.FileLoader(pathes)
    assert loader.path != None
    fileList = loader.getCsvFilesList()
    assert fileList is not None
    assert len(fileList) > 0

def test_csv_read(pathes):
    loader = dkb.DKB() 
    assert loader is not None
    df=loader.get_dkb_df(pathes / 'tst.csv') # not utf-8 encoded
    assert df is not None
    dic = loader.get_meta(pathes / 'tst.csv')
    assert dic["Kontonummer"] != ""
    '''
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfc in position 226: invalid start byte
    
    df = loader.get_dkb_df_from_folder(pathes) 
    assert len(loader.csv_files) > 0
    assert df is not None 
    '''

def test_orm_import_in_db(pathes):
    loader = dkb.DKB()
    csv_df = loader.get_dkb_df(pathes / 'tst.csv')
    o = orm.DB_Handler(pathes, 'new_db_from_test', 'sqlite3')
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
    o = orm.DB_Handler(pathes, 'db4test', 'sqlite3')
    # data = o.get_month('2016', '04')
    # assert len(data) > 0
    o.update_engine()
    data = o.get_class()
    assert len(data) > 0
    assert data[0] == 'test1'
'''
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
    loader = dkb.DKB(pathes)
    df=loader.parseDkbData()

    # assert db.importNewData(df) == True

'''