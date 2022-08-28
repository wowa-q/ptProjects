
import pytest
from pathlib import Path

from src.dkb.fileLoader import FileLoader
from src.dkb.dkb import DKB
from src.dkb.db import DB

@pytest.fixture
def pathes():
    pth = Path('D:/005-pj/ptpj/ptProjects/test/fixtures')
    return pth

def test_FileLoaderInitialization(pathes):
    loader = FileLoader('')
    assert loader.path != None
    assert loader.fileList != None
    assert len(loader.fileList) == 0
    loader = FileLoader(pathes)
    assert loader.path != None
    assert loader.fileList != None
    assert len(loader.fileList) > 0
    for csv in loader.fileList:
        print(csv)

def test_csvRead(pathes):
    loader = DKB(pathes) 
    assert loader != None
    loader.parseDkbData()
    assert len(loader.csv_files) > 0

def test_dbConnection(pathes):
    db = DB(pathes, 'test_db', 'sqlite3')
    assert db != None
    check = db.createConnection()
    assert check == True
    db_file = Path(pathes / 'test_db.db')
    assert db_file.is_file() == True
    
def test_dbTableCreate(pathes):
    db = DB(pathes, 'test_db', 'sqlite3')
    check = db.createConnection()
    db.createNewTable('category')

def test_dbImportDF(pathes):
    db = DB(pathes, 'test_db', 'sqlite3')
    check = db.createConnection()
    loader = DKB(pathes)
    loader.parseDkbData()

'''-----------------------------------------------------------'''
def add(numbers):
    result =  0
    for num in numbers:
        result +=num    
    return result

@pytest.fixture
def nums():
    return [1,2,3]

def test_fixures(nums):
    assert add(nums) == 6