from openpyxl import Workbook, load_workbook
import pathlib

   

PROJEC_DIRECTORY_PATH = pathlib.Path(__file__).parent.parent.parent.resolve()
fix_path = PROJEC_DIRECTORY_PATH / 'test/fixtures'
xls_file = fix_path / 'haushalt.xlsm'
print (xls_file)

wb = load_workbook(xls_file, read_only=False, keep_vba=True)
title= wb['title']
# print(sheets)
# title = wb.active
title['H10'] = "Python executed: ExcelWriter initialized"
#xls_file = fix_path / 'haushalt1.xlsm'
wb.save(xls_file)