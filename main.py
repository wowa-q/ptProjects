# -*- coding: iso-8859-1 -*-

from pathlib import Path
# user packages:
from dkb.dkb import DKB
from dkb.db import DB
import dkb.orm as orm
from fl.fileLoader import FileLoader

if __name__ == '__main__':
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    dkb_csv = DKB(pth)
    print('# dkb object created #')
    csv_df = dkb_csv.parseDkbData()
    
    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    o = orm.DB_Handler(db_file, 'new-db', 'sqlite3')
    assert o != None
    o.importDKBDF(csv_df)