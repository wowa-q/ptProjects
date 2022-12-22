# pylint: disable=wrong-import-order
# pylint: disable=unused-import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pathlib
from unittest.mock import Mock

import pytest

# user packages
from .context import dkb
from . import dbfixes as fx

# pylint: disable=wrong-import-order

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"

def test_add(fx_cat_dict, fx_cat_handler): # pylint: disable=missing-function-docstring
    fx_cat_handler.add(fx_cat_dict)
    result = fx_cat_handler.get_row_by_name(fx_cat_dict['name'])
    assert result is not None, "No return from the table received" 
    assert len(result[0]) != "", f"Category {fx_cat_dict['name']} not found in the table" 


def test_get_len(fx_cat_dict, fx_cat_handler): # pylint: disable=missing-function-docstring
    result1 = fx_cat_handler.get_table_length()
    fx_cat_handler.add(fx_cat_dict)
    result2 = fx_cat_handler.get_table_length()
    assert result2 is not None, "Category table has no entries as expected"
    assert result2 > result1, "Category length was not increased"

def test_update(fx_cat_dict, fx_cat_handler): # pylint: disable=missing-function-docstring
    fx_cat_handler.add(fx_cat_dict)
    fx_cat_handler.update_row(fx_cat_dict['name'], type='updated')
    result = fx_cat_handler.get_row_by_name(fx_cat_dict['name'])
    assert result['type'] == 'updated', f"Entry {fx_cat_dict['name']}, type was not updated"
    fx_cat_handler.update_row(fx_cat_dict['name'], cycle='updated')
    result = fx_cat_handler.get_row_by_name(fx_cat_dict['name'])
    assert result['cycle'] == 'updated', f"Entry {fx_cat_dict['name']}, cycle was not updated"
    fx_cat_handler.update_row(fx_cat_dict['name'], type='1-updated', cycle='2-updated')
    result = fx_cat_handler.get_row_by_name(fx_cat_dict['name'])
    assert result['cycle'] == '2-updated', f"Entry {fx_cat_dict['name']}, cycle was not updated"
    assert result['type'] == '1-updated', f"Entry {fx_cat_dict['name']}, type was not updated"



# def test_add_x_rows(): # pylint: disable=missing-function-docstring

