# -*- coding: iso-8859-1 -*-

from pathlib import Path
# user packages:
from dkb.dkb import DKB
from dkb.db import DB
from fl.fileLoader import FileLoader

if __name__ == '__main__':
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    dkb_csv = DKB(pth)
    print('# dkb object created #')
    dkb_csv.parseDkbData()
    # dkb_csv.getDF()

    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    db = DB(db_file, 'main_DB', 'sqlite3')
    db.createTable('types')

