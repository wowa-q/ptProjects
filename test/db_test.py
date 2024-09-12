# pylint: skip-file

import pathlib
from unittest.mock import Mock

import pytest

# user packages
from .context import dkb
from . import dbfixes as fx
# package to test
from dkb.db import db_api as db


FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"


def test_db_created(fx_db_file2create):
    # test: new db file with tables can be created  
    fileList=list(FIXTURE_DIR.glob('**/*.db'))
    before = len(fileList)
    db_handler = db.DbHandler(FIXTURE_DIR)
    db_handler.create_db(fx_db_file2create)
    fileList=list(FIXTURE_DIR.glob('**/*.db'))
    after = len(fileList)  
    assert before < after, "no new db was created"

def test_import_single_class(fx_classes_dict, fx_db_file2modify):
    #test: new class can be added
    db_handler = db.DbHandler(fx_db_file2modify)    
    db_handler.create_classes(fx_classes_dict)
    result = db_handler.get_class_from_classes_by_name(fx_classes_dict['name'])    
    db_handler.close()     
    assert result is not None, f"Class: {fx_classes_dict['name']} in Classes Table couldn't be found "

def test_import_single_cat(fx_cat_dict, fx_db_file2modify): 
    # test: new category can be added
    db_handler = db.DbHandler(fx_db_file2modify)    
    db_handler.create_category(fx_cat_dict)
    result = db_handler.get_cat_from_category_by_name(fx_cat_dict['name'])
           
    db_handler.close()
    assert result is not None, f"Class: {fx_cat_dict['name']} in Category Table couldn't be found "

def test_create_new_single_meta(fx_meta_dict, fx_db_file2modify): 
    # test: new meta entry can be added 
    db_handler = db.DbHandler(fx_db_file2modify)    
    db_handler.create_csv_meta(fx_meta_dict)
    result = db_handler.find_checksum(fx_meta_dict['checksum'])    
    db_handler.close()     
    assert len(result[1]) > 0, f"Meta Entry: {fx_meta_dict['checksum']} in Meta Table couldn't be found "
