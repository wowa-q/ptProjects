# -*- coding: iso-8859-1 -*-
'''
Created on 01.09.2022

@author: wakl8754
'''
import pandas as pd # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
from pathlib import Path

# user packages:
from fl.fileLoader import FileLoader

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