# -*- coding: iso-8859-1 -*-
'''
Created on 22.06.2021

@author: wakl8754
'''

import pandas as pd # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
from pathlib import Path
from src.dkb import fileLoader as fl



class CsvImporter(object):
    '''
    Performs parsing of the CSV file from DKB
    '''
    # the line here to find header line
    __header_line = 6               
    # headers to map
    __header = ['date',
                'booking-date',
                'text',
                'debitor',
                'verwendung',
                'konto',
                'blz',
                'value',
                'debitor-id',
                'Mandatsreferenz',
                'Customer reference']
    def __init__(self, pth):
        ''' @pth input pathlib.Path type see https://docs.python.org/3/library/pathlib.html 
            pth to the folder with csv files path shall of the type pathlib.Path
        '''
        self.csv_files = fl.FileLoader(pth).fileList
        #self.csv_file = self.csv_files[0]
        
    def parseDkbData(self):
        for csv in self.csv_files:
            self._getData(csv)

    def _getData(self, csv_file):       
        '''
        reads the CSV file and creates data frame with the parsed data. Panda df is returned.
        https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
        '''
        
        try:
            df = pd.read_csv(csv_file,
                  skiprows = self.__header_line+1,                  
                  encoding=None, # needs to be None to be able to read German text                  
                  warn_bad_lines=True,
                  delimiter=";",
                  parse_dates = [0,1]
                )
            df.columns = self.__header
            print('DATA FRAME created')
            #print(df.columns)
            #print(df.count())
            return df
        except: 
            print(f"File not found at: {csv_file}, or file is corrupted")
            return None
        
    
