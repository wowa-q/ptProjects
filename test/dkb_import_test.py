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
    assert fileList != None
    assert len(fileList) == 0
    # folder with csv files 
    loader = fl.FileLoader(pathes)
    assert loader.path != None
    fileList = loader.getCsvFilesList()
    assert fileList != None
    assert len(fileList) > 0

def test_csvRead(pathes):
    loader = dkb.DKB(pathes) 
    assert loader != None
    loader.parseDkbData()
    assert len(loader.csv_files) > 0
    assert loader._checkDkbFormat(pathes / "tst.csv") == True
    dict = loader.getMeta(pathes / "tst.csv")
    assert dict["Kontonummer"] != ""

def test_dbConnection(pathes):
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

def test_orm(pathes):
    loader = dkb.DKB(pathes)
    csv_df = loader.parseDkbData()
    
    o = orm.DB_Handler(pathes, 'new-db', 'sqlite3')
    assert o != None
    o.importDKBDF(csv_df)