import pytest
from pathlib import Path

# user packages
import dkb.dkb as dkb
import dkb.db as sq
import fl.fileLoader as fl



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
    check = db._createConnection()
    loader = dkb.DKB(pathes)
    loader.parseDkbData()