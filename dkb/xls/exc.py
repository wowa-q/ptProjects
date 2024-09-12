# -*- coding: iso-8859-1 -*-
'''
Created on 01.09.2022

@author: wakl8754
'''
import xlwings as xw
# user packages:

class ExcelCfg():
    ''' configuration of the excel tables '''
    _gesamtkosten_table = {'start':'A1', 'stop': 'C1'}
    _account_wowa = {'start': 'A7', 'stop': 'C7'}

class ExcelWriter():
    '''
    class to write into existing Excel by using xlwings
    '''
    def __init__(self, xls_file) -> None:
        self.work_book = xw.Book(xls_file)
        # -------------------------------------- #
        sheet_test = self.work_book.sheets("title")
        sheet_test ['H1'].value = "Python executed: ExcelWriter initialized"

    @staticmethod    
    def write_meta(sheet, meta_dict):
        ''' 
        Writes meat data into the given sheet
        @sheet sheet object from the work book to which the meta data shall be written 
        @meta_dict dictionary produced by DKB.get_meta(csv)
        '''
        ctr = 1
        for key in meta_dict:
            cell1 = 'A'+str(ctr)
            cell2 = 'B'+str(ctr)        
            sheet[cell1].value = key
            sheet[cell2].value = meta_dict[key]
            ctr += 1
    
    def create_new_sheet(self, name: str, after: str):
        '''
        Creates a new sheet if it doesn not exist after @after sheet
        returns new sheet
        @name name of the sheet to be returned
        @after name of the sheet after which new shall be created
        '''
        try:
            sheet = self.work_book.sheets(name)
        except:
            sheet = self.work_book.sheets.add(name=name, before=None, after=after)
        return sheet

    @staticmethod
    def write_month(sheet, data):
        ''' write month data from db to excel 
        @sheet name of the excel sheet in the workbook
        @data data extracted from db
        '''
        cells = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for ln_ctr, rdata in enumerate(data, start=5):
            for cell, val in zip(cells, list(rdata)):
                sheet[cell+str(ln_ctr)].value = str(val)