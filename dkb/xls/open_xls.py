""" what is the module about? """
from openpyxl import load_workbook
#from openpyxl import Workbook

class ExcelCfg():
    _gesamtkosten_table = {'start':'A1', 'stop': 'C1'}
    _account_wowa = {'start': 'A7', 'stop': 'C7'}
    xls_attr = {'as_template': False, 
                'macro': True,
                'extension' : 'xlsm'
                }


class ExcelWriter():
    '''
    class to write into existing Excel by using xlwings
    '''
    def __init__(self, xls_file) -> None:
        self.xls_file = xls_file
        self.work_book = load_workbook(xls_file, read_only=False, keep_vba=True)
        # -------------------------------------- #
        # title = self.work_book['title']
        # title['H10'] = "Python executed: ExcelWriter initialized"
        # self.work_book.save(xls_file)
    # pylint: disable=unused-argument, bare-except, missing-function-docstring
    def create_new_sheet(self, name: str, after: str):
        try:
            sheet = self.work_book[name]
        except:
            sheet = self.work_book.create_sheet(name)
        return sheet

    def write_month(self, sheet, data):
        print(sheet)
        cells = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for ln_ctr, rdata in enumerate(data, start=5):
            for cell, val in zip(cells, list(rdata)):
                sheet[cell+str(ln_ctr)] = val
        self.work_book.save(self.xls_file)
