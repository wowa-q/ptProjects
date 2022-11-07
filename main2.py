# -*- coding: iso-8859-1 -*-

from pathlib import Path
import argparse

# user packages:
from dkb.dkb import DKB
import dkb.orm as orm
from dkb.exc import ExcelWriter 
import api

DEBUGLEVEL = 2



if __name__ == '__main__':
    # Create Receiver objects    
    pth = Path('D:/005-pj/ptpj/api/ptProjects/test/fixtures')
    db_file = Path('D:/005-pj/ptpj/api/ptProjects/test/fixtures')
    xls_file=r"d:\005-pj\ptPj\api\ptProjects\test\fixtures\haushalt.xlsm"
    db_name = 'new__main2db'
    dkb_ld = DKB(pth)    
    orm = orm.DB_Handler(db_file, db_name, 'sqlite3')
    writer = ExcelWriter(xls_file)
    
    invoker = api.Invoker()
    
    # Parametrize the Invoker and execute the command
    parser = argparse.ArgumentParser(description='Parametrizing the Invoker')
    parser.add_argument('--cmd', metavar='name', required=True,
                        help='the command to be executed')
    parser.add_argument('--year', metavar='name', required=False,
                        help='year e.g. 2022') 
    parser.add_argument('--month', metavar='name', required=False,
                        help='month as a number e.g. 01')                       
    args = parser.parse_args()
    cmd = args.cmd
    if cmd in "Create-new-DB":
        # invoker.set_on_start(api.CmdCheckFileSystem(receiver = db_file / 'new__main2db.db'))
        invoker.set_main_command(api.CmdCreateNewDB(dkb_ld, orm))
    elif cmd in "Create-new-Jan":
        invoker.set_main_command(api.CmdNewMonth(dkb_ld, orm, writer, 
                                                "Jan"))       
    elif cmd in "Create-new-Month":
        month = str(args.year) + '-' + str(args.month)+'-'
        
        invoker.set_main_command(api.CmdNewMonth(dkb_ld, orm, writer, 
                                                args.year,  args.month)) 
    invoker.run_commands()