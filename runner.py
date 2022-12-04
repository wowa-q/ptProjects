import argparse
# user packages:
from dkb.cfg import Project
from dkb.db import db_api 
from dkb.dkb import DKB
from dkb.xls import exc
from dkb.xls import open_xls as xls
from dkb import api

DEBUGLEVEL = 2

# Create Receiver objects    
pth = Project.PROJEC_DIRECTORY_PATH.value
fix_path = Project.PROJEC_DIRECTORY_PATH.value.parent.resolve() / 'dkb_p'

invoker = api.Invoker()
# Parametrize the Invoker and execute the command
parser = argparse.ArgumentParser(description='Parametrizing the Invoker')

parser.add_argument('--cmd', metavar='name', required=True,
                        help='the basic command to be executed')
parser.add_argument('--year', metavar='name', required=False,
                        help='year e.g. 2022') 
parser.add_argument('--month', metavar='name', required=False,
                        help='month as a number e.g. 01')
parser.add_argument('--csv_name', metavar='name', required=False,
                        help='csv file name, incl. ".csv"')
parser.add_argument('--db_name', metavar='name', required=False,
                        help='db file name, incl. ".db"') 
args = parser.parse_args()
cmd = args.cmd
# parametrize the invoker and commands
if cmd in "Create-new-DB": # cli test passed, excel failed
    ''' --cmd Create-new-DB --db_name example.db '''
    db_file = fix_path / args.db_name
    db_handler = db_api.DB_Handler(db_file)
    invoker.set_main_command(api.CmdCreateNewDB(db_handler,db_file))
elif cmd in "Import-new-csv": # cli test passed, excel failed
    ''' --cmd Import-new-csv --db_name example.db --csv_name 1001670080.csv '''
    print(' # start execution Import-new-csv # ')
    csv_file = fix_path / 'csv' / args.csv_name
    db_file = fix_path / args.db_name
    db_handler = db_api.DB_Handler(db_file)
    dkb_ld = DKB()
    print(f'Import-new-csv: {csv_file}')
    invoker.set_main_command(api.CmdImportNewCsv(db_handler, dkb_ld, csv_file))
    invoker.set_on_finish(api.CmdArchiveCsv(csv_file))
elif cmd in "Create-new-Month": # cli test passed, excel passed
    ''' --cmd Create-new-Month --db_name example.db --year 2016 --month 01'''
    month = str(args.month)
    year = str(args.year)
    db_file = fix_path / args.db_name
    xls_file = fix_path / 'haushalt.xlsm'
    db_handler = db_api.DB_Handler(db_file)
    # writer = exc.ExcelWriter(xls_file) 
    writer = xls.ExcelWriter(xls_file)
    invoker.set_main_command(api.CmdNewMonth(db_handler, writer, year, month))
else:
    # branch for quick testing:
    ''' --db_name example.db '''
    # db_file = fix_path / args.db_name
    xls_file = fix_path / 'haushalt.xlsm'
    # db_handler = db_api.DB_Handler(db_file)
    writer = xls.ExcelWriter(xls_file) 
    # invoker.set_main_command(api.CmdNewMonth(db_handler, writer, year, month))


# runs the configutred command
invoker.run_commands()