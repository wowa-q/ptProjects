# pylint: skip-file
import pathlib

import pytest

from .dbfixes import fx_db_file2create
from .dbfixes import fx_db_file2copy
from .dbfixes import fx_db_file2modify
from .dbfixes import fx_classes_dict
from .dbfixes import fx_cat_dict
from .dbfixes import fx_meta_dict
from .dbfixes import fx_dkb_line
from .dbfixes import fx_db_api
from .dbfixes import fx_cat_handler
from .dbfixes import fx_class_handler
from .dbfixes import fx_meta_handler
from .dbfixes import fx_dkb_handler
from .dbfixes import fx_archive

from .xlsfixes import fx_xls_file2create
from .xlsfixes import fx_xls_owriter
from .xlsfixes import fx_month_data
from .xlsfixes import fx_xls_template

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve() / "fixtures"