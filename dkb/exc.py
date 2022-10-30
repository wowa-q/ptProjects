# -*- coding: iso-8859-1 -*-
'''
Created on 01.09.2022

@author: wakl8754
'''
import pandas as pd # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
from pathlib import Path
import xlwings as xw


# user packages:


class ExcelWriter(object):
    '''
    class to write into existing Excel by using xlwings
    '''
    def __init__(self, xls_file) -> None:
        '''
        @xls_path = r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm")
        '''
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
    
    def createSheet(self, name, after):
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


class ExcelLoader(object):
    '''
    class to create Excel by using Pandas Data Frame
    '''
    def __init__(self, df=None) -> None:
        if df:
            self.df = df
    
    def setExcelParam(self, excel_path, sheet_name):
        self.excel_writer = excel_path
        self.sheet_name = sheet_name
    
    def createExcel(self):
        self.df.to_excel(self.excel_wrtier,
                        self.sheet_name,
                        engine='openpyxl',
                        freeze_panes=(1,1))