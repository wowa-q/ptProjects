"""The module shall hold the fixtures, which can be used in the test"""
# pylint: skip-file

import pathlib
import shutil
import random
import time
from datetime import datetime
# 3rd party
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dkb.db import db_api as db
from dkb.db.category_table import CategoryTableHandler
from dkb.db.class_table import ClassesTableHandler
from dkb.db.meta_table import CsvMetaTableHandler
from dkb.db.dkb_table import DkbTableHandler

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"

@pytest.fixture
def fx_db_file2create():
    """Definitiaon of db file, which shall be created and deleted when the test was done

    Yields:
        path string: file path
    """
    db_file = FIXTURE_DIR / "test_db_created.db"
    yield db_file 
    # delete the modified db file and copy one to make repeat of the test possible
    try:
        db_file.unlink()
    except FileNotFoundError:
        pass

@pytest.fixture
def fx_db_file2copy():
    """Path to db file, which is used as template to create new db files by copying this template

    Returns:
        path string: file path
    """
    return FIXTURE_DIR / "db2test_copy.db"

@pytest.fixture
def fx_db_file2modify(fx_db_file2copy):
    """Provides path to the db file, which shall be modified. The file will be reporodcued by copying the template after the test, to make the test repeatable.

    Args:
        db_file2copy (path): path to the template file

    Yields:
        path string: file path to db, which should be modified during the test
    """
    db_file = FIXTURE_DIR / "db4test.db"
    yield db_file 
    # delete the modified db file and copy one to make repeat of the test possible
    db_file.unlink()
    shutil.copy(fx_db_file2copy, db_file)

@pytest.fixture
def fx_classes_dict():
    """provides valid dict for Classes table, representing a line

    Returns:
        dict: dictionary for Classes table entries
    """
    ln_dict = {}
    ln_dict['inout'] = 'IN'
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['fix'] = 'TRUE'
    return ln_dict

@pytest.fixture
def fx_cat_dict():
    ln_dict = {}
    ln_dict['type'] = 'Steuer'
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['cycle'] = 'yearly'
    return ln_dict

@pytest.fixture
def fx_meta_dict():
    ln_dict = {}
    ln_dict['date'] = datetime.now()
    ln_dict['name'] = 'test_import_single_line'
    ln_dict['konto'] = 'yearly'
    # ln_dict['checksum'] = '12345'
    ln_dict['checksum'] = random.randint(100000, 1000000)
    return ln_dict

@pytest.fixture
def fx_dkb_line():
    ln = "27.06.2016;27.06.2016;GUTSCHRIFT;OLGA MERKEL;Dankee rest folgt;DE15410500950001708361;WELADED1HAM;190;;;NOTPROVIDED"

@pytest.fixture
def fx_db_api(fx_db_file2copy, fx_db_file2modify):
    db_handler = db.DbHandler(fx_db_file2modify)
    yield db_handler
    db_handler.close()
    time.sleep(2)
    fx_db_file2modify.unlink()
    shutil.copy(fx_db_file2copy, fx_db_file2modify)

@pytest.fixture
def fx_cat_handler(fx_db_file2copy, fx_db_file2modify):
    dkb_engine = create_engine('sqlite:///' + str(fx_db_file2modify), echo=True)
    dkb_session = sessionmaker(bind=dkb_engine) 
    handler = CategoryTableHandler(dkb_session, dkb_engine)
    yield handler
    dkb_session.close_all() 
    time.sleep(2)
    fx_db_file2modify.unlink()
    shutil.copy(fx_db_file2copy, fx_db_file2modify)

@pytest.fixture
def fx_class_handler(fx_db_file2copy, fx_db_file2modify):
    dkb_engine = create_engine('sqlite:///' + str(fx_db_file2modify), echo=True)
    dkb_session = sessionmaker(bind=dkb_engine) 
    handler = ClassesTableHandler(dkb_session, dkb_engine)
    yield handler
    dkb_session.close_all() 
    time.sleep(2)
    fx_db_file2modify.unlink()
    shutil.copy(fx_db_file2copy, fx_db_file2modify)

@pytest.fixture
def fx_meta_handler(fx_db_file2copy, fx_db_file2modify):
    dkb_engine = create_engine('sqlite:///' + str(fx_db_file2modify), echo=True)
    dkb_session = sessionmaker(bind=dkb_engine) 
    handler = CsvMetaTableHandler(dkb_session, dkb_engine)
    yield handler
    dkb_session.close_all() 
    time.sleep(2)
    fx_db_file2modify.unlink()
    shutil.copy(fx_db_file2copy, fx_db_file2modify)

@pytest.fixture
def fx_dkb_handler(fx_db_file2copy, fx_db_file2modify):
    dkb_engine = create_engine('sqlite:///' + str(fx_db_file2modify), echo=True)
    dkb_session = sessionmaker(bind=dkb_engine) 
    handler = DkbTableHandler(dkb_session, dkb_engine)
    yield handler
    dkb_session.close_all() 
    time.sleep(2)
    fx_db_file2modify.unlink()
    shutil.copy(fx_db_file2copy, fx_db_file2modify)


@pytest.fixture
def fx_archive():    
    csv_file = FIXTURE_DIR / 'move_temp.csv'
    shutil.copy(FIXTURE_DIR / 'move.csv', csv_file)
    zip_file = FIXTURE_DIR / 'archive.zip'
    yield zip_file, csv_file
    zip_file.unlink()