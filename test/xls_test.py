# pylint: skip-file
import os
import pathlib
import hashlib
from unittest.mock import Mock

import pytest

# user packages
from .context import dkb
from . import xlsfixes as fx
from dkb.xls import open_xls as oxls

def test_create_new_xls(fx_xls_file2create, fx_month_data):
    writer = oxls.ExcelWriter(fx_xls_file2create)
    sheet=writer.create_new_sheet(name='Jan', after=None)
    writer.write_month(sheet, fx_month_data)
    assert isinstance(fx_xls_file2create, os.PathLike)==True, 'no file was created'

    # Check if we were passed a file-like object
    # if isinstance(file, os.PathLike):
    #     file = os.fspath(file)
    # if isinstance(file, str):
        