# -*- coding: iso-8859-1 -*-

from pathlib import Path
from turtle import title

# user packages:
from dkb.dkb import DKB
import dkb.orm as orm
from dkb.exc import ExcelWriter 

DEBUGLEVEL = 2



if __name__ == '__main__':
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    dkb_ld = DKB(pth)
    print('# dkb object created #')
    csv_df = dkb_ld.parseDkbData()
    
    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    o = orm.DB_Handler(db_file, 'new-db', 'sqlite3')
    assert o != None
    o.importDKBDF(csv_df)
    
    csv_file = 'D:/005-pj/ptpj/dkb/ptProjects/test/fixtures/tst.csv'    
    writer = ExcelWriter(xls_file=r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm")
    sheet = writer.createSheet('Month', after='title')
    writer.writeMeta(sheet, dkb_ld.getMeta(csv_file))
    