# pylint: skip-file
'''
https://www.youtube.com/watch?v=xT4SV7AH3G8
'''
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
import random

# user packages
from .context import dkb
# from dkb.db import db_api as db
# # from dkb.db.constructor import Base
# from dkb.db import dkb_table, class_table 
# from dkb import dkb
# from dkb import api
from sandbox import mocking

@patch('sandbox.mocking.fun_to_be_mocked')
def test_Mock_basic(mock_fun_to_be_mocked):
    # pytest.skip('not correct test')
    mock_fun_to_be_mocked.return_value = 4
    assert mocking.fun_to_be_tested() == 7, "fun_to_be_mocked returned other than 3"
    

@patch('sandbox.mocking.fun_to_be_mocked')
def test_Mock_instance(mock_fun_to_be_mocked):
    # to mock the class which is to be used by the dut
    mc_instance = MagicMock()
    # it accepts all attributes and creates them dynamically
    mc_instance.my_attr = 200
    mc_instance.my_method.return_value = "return value"

    mock_fun_to_be_mocked.return_value = 4
    assert mocking.fun_to_be_tested() == 7, "fun_to_be_mocked returned other than 3"