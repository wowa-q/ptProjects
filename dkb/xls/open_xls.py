
from openpyxl import Workbook, load_workbook


class ExcelCfg(object):
    _gesamtkosten_table = {'start':'A1', 'stop': 'C1'}
    _account_wowa = {'start': 'A7', 'stop': 'C7'}
    xls_attr = {'as_template': False, 
                'macro': True,
                'extension' : 'xlsm'
                }


class ExcelWriter(object):
    '''
    class to write into existing Excel by using xlwings
    '''
    def __init__(self, xls_file) -> None:
        self.xls_file = xls_file
        self.wb = load_workbook(xls_file, read_only=False, keep_vba=True)
        # -------------------------------------- #
        # title = self.wb['title']
        # title['H10'] = "Python executed: ExcelWriter initialized"
        # self.wb.save(xls_file)
            
    def create_new_sheet(self, name: str, after: str):
        try:
            sheet = self.wb[name]
        except:
            sheet = self.wb.create_sheet(name)
        return sheet
    
    def write_month(self, sheet, data):
        print(sheet)
        cells = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for ln_ctr, dt in enumerate(data, start=5):
            for cell, val in zip(cells, list(dt)):
                sheet[cell+str(ln_ctr)] = val        
        self.wb.save(self.xls_file)