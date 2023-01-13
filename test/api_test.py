# pylint: skip-file
import os
import pathlib
import hashlib
from unittest.mock import Mock

import pytest

# user packages
from .context import dkb
from . import dbfixes as fx
# package to test
from dkb.db import db_api as db
from dkb.dkb import Dkb
import dkb.api

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"


def test_import_csv(fx_db_api):
    '''
    - import the valid csv
    - new meta data entry was created
    '''
    db_handler = fx_db_api
    dkb_ld = Dkb()
    cmd = dkb.api.CmdImportNewCsv(db_handler, dkb_ld, FIXTURE_DIR / 'test1.csv')
    cmd.execute()

    with open(str(FIXTURE_DIR / 'test1.csv'), 'rb') as file:
        # calculate first the checksum of the given csv file
        checksum = hashlib.md5(file.read()).hexdigest().upper()
    result = db_handler.find_checksum('123456789')
    assert len(result[1]) == 0, "Checksum could unexpectedly be found"
    # check if checksum is imported into table
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
        checksum = hashlib.md5(file.read()).hexdigest().upper()
    result = db_handler.find_checksum(checksum)
    assert len(result[1]) == 1, f"Checksum could not be found \
                                checksum: {checksum}"
    result = db_handler.get_month('2016', '06')

    assert len(result[1]) == 9, f"Number of imported items is {len(result[1])} \
                                imported from {FIXTURE_DIR} \
                                entries: {result[1]}"


def test_csv_moved(fx_archive):
    zip_file, csv_file = fx_archive
    cmd_archive = dkb.api.CmdArchiveCsv(csv_file, zip_file)
    cmd_archive.execute()
    # check new archive was created
    assert os.path.isfile(zip_file) == True, f"zip file wasn't created"
    # check csv file was deleted, after beeing archived
    assert os.path.isfile(csv_file) == False, f"File wasn't moved"
