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
    # dkb_ld = DKB(pth)
    dkb_loader = DKB()
    dkb_df = dkb_loader.get_dkb_df_from_folder(pth)
    dkb_df = dkb_loader.get_dkb_df(pth / 'tst.csv')
    
    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    o = orm.DB_Handler(db_file, 'new-db', 'sqlite3')
    assert o != None
    
    # DB methods
    o.createClassTable()
    o.createDkbMetaTable()
    o.createCathTable()
    o.createTables()
    o.importDKBDF(dkb_df)
    print(o._checkColumnExists('DKBTable', 'Class'))

    # o.addClassColumn()
    # o.addCathColumn()

    cath_table = ['Versicherung', 4]
    class_data = ['out', 'bla', 'fix', 'lastschrift']
    o.addNewClass(class_data)
    # class_data = ['out', 'bla', 'var', 'lastschrift']
    # o.addNewClass(class_data)
    # o.addNewCath(["versicherung", 4])
    
    # Excel methods
    csv_file = 'D:/005-pj/ptpj/dkb/ptProjects/test/fixtures/tst.csv'    
    writer = ExcelWriter(xls_file=r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm")
    sheet = writer.createSheet('Month', after='title')
    writer.writeMeta(sheet, dkb_loader.getMeta(csv_file))
    