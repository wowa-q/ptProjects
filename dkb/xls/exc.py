# -*- coding: iso-8859-1 -*-
'''
Created on 01.09.2022

@author: wakl8754
'''
import xlwings as xw


# user packages:

class ExcelCfg(object):
    _gesamtkosten_table = {'start':'A1', 'stop': 'C1'}
    _account_wowa = {'start': 'A7', 'stop': 'C7'}

class ExcelWriter(object):
    '''
    class to write into existing Excel by using xlwings
    '''
    def __init__(self, xls_file) -> None:
        self.wb = xw.Book(xls_file)
        # -------------------------------------- #
        sheet_test = self.wb.sheets("title")
        sheet_test ['H1'].value = "Python executed: ExcelWriter initialized"
        
    def writeMeta(self, sheet, metaDict):
        ''' 
        Writes meat data into the given sheet
        @sheet sheet to which the meta data shall be written
        @metaDict dictionary produced by DKB.getMeta(csv)
        '''
        ctr = 1
        for key in metaDict:
            cell1 = 'A'+str(ctr)
            cell2 = 'B'+str(ctr)        
            sheet[cell1].value = key
            sheet[cell2].value = metaDict[key]
            ctr += 1
    
    def create_new_sheet(self, name: str, after: str):
        '''
        Creates a new sheet if it doesn not exist after @after sheet
        returns new sheet
        @name name of the sheet to be returned
        @after name of the sheet after which new shall be created
        '''
        try:
            sheet = self.wb.sheets(name)
        except:
            sheet = self.wb.sheets.add(name=name, before=None, after=after)
        return sheet

    def write_month(self, sheet, data):
        cells = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for ln_ctr, dt in enumerate(data, start=5):
            for cell, val in zip(cells, list(dt)):
                sheet[cell+str(ln_ctr)].value = str(val)