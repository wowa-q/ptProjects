import pytest
from pathlib import Path

# user packages
import dkb.dkb as dkb
import dkb.db as sq
import fl.fileLoader as fl
import dkb.orm as orm
import api as api

@pytest.fixture
def pathes():
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    return pth

def test_newDBcmd(pathes):
    # pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures/new_Invoker_db.db')
    # xls_file=r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm"
    db_name = 'new_Invoker_db'
    dkb_ld = dkb.DKB(pathes)    
    o = orm.DB_Handler(pathes, db_name, 'sqlite3')    
    invoker = api.Invoker()
    invoker.set_on_start(api.CmdCheckFileSystem())
    invoker.set_main_command(api.CmdCreateNewDB(dkb_ld, o))
    assert db_file.is_file() == True

    layers_name = r"\new_Invoker_db.db"
    layers_folder = Path(pathes, layers_name)
    assert layers_folder.exists() == True