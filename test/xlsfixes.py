# pylint: skip-file
"""The module shall hold the fixtures, which can be used in the test"""


import pathlib
import shutil
import random
import time
from datetime import datetime
# 3rd party
import pytest
from openpyxl import Workbook

from dkb.xls import open_xls as oxls

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"

@pytest.fixture
def fx_xls_file2create():
    """Definitiaon of excel file, which shall be created and deleted when the test was done

    Yields:
        path string: file path
    """
    xls_file = FIXTURE_DIR / "test_haushalt.xlsx"
    yield xls_file 
    # delete the modified db file and copy one to make repeat of the test possible
    # try:
    #     xls_file.unlink()
    # except FileNotFoundError:
    #     pass

@pytest.fixture
def fx_xls_owriter(fx_xls_file2create):
    writer = oxls.ExcelWriter(fx_xls_file2create)
    yield writer
    fx_xls_file2create.unlink()

@pytest.fixture
def fx_month_data():
    month_data = []
    month_data_header = [
        'id',
        'date',
        'booking-date',
        'text',
        'debitor',
        'verwendung',
        'konto',
        'blz',
        'value',
        'debitor-id',
        'mandat',
        'customer',
        'class',
        'category'
    ]
    month_data_row = []
    
    month_data.append(month_data_header)
    # for i in range(10):
    #     for i in range(1, 14):
    #         month_data_row.append(random.randint(1, 100))
    #     month_data.append(month_data_row)
    return month_data

@pytest.fixture
def fx_xls_template(fx_xls_file2create):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.title='Jan'
    for irow in range(10):
        ws.append(['%d' % i for i in range(12)])
    wb.save(fx_xls_file2create)