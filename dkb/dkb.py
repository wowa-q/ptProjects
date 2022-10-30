# -*- coding: iso-8859-1 -*-
'''
Created on 22.06.2021

@author: wakl8754
'''
from typing import Any
import pandas as pd 
import csv
# import user packages
from fl.fileLoader import FileLoader


DEBUGLEVEL = 1
INFO = False

class DKB(object):
    '''
    Performs parsing of the CSV file from DKB
    '''
    # the line here to find header line
    __header_line = 6               
    # headers to map
    __header = [
                'date',
                'booking-date',
                'text',
                'debitor',
                'verwendung',
                'konto',
                'blz',
                'value',
                'debitor-id',
                'Mandats reference',
                'Customer reference']
    def __init__(self, pth):
        ''' @pth input pathlib.Path type see https://docs.python.org/3/library/pathlib.html 
            pth to the folder with csv files path shall of the type pathlib.Path
        '''        
        self.loader = FileLoader(pth)
                
    def parseDkbData(self):
        pieces = []
        df = None
        
        self.csv_files = self.loader.getCsvFilesList()
        if len(self.csv_files) == 0:
            if DEBUGLEVEL > 0: print('# list of files is empty #')
            return None
        for csv in self.csv_files:
            df = self._getData(csv)
            if df is not None:
                pieces.append(df)
        if len(pieces) == 1:
            return df
        elif len(pieces) > 1:     
            if INFO: print('# parseDkbData: # Concatenate DataFrames with panda #')       
            return pd.concat(pieces)
        else:
            if DEBUGLEVEL > 0: print('# parseDkbData: # list of pieces is empty #')
            return df
    
    def getDF(self):
        self.csv_files = self.loader.getCsvFilesList()
        self._getData(self.csv_files[0])
    
    def getMeta(self, csv_file):
        dkb_format = self._checkDkbFormat(csv_file)
        if dkb_format:
            self.metaDic = {
                "Kontonummer" : "",
                "Von" : "",
                "Bis" : "",
                "Kontostand" : ""
            }
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                nrLines = 0
                for row in reader:
                    # if "Kontonummer" in row:
                    if nrLines == 0:
                        self.metaDic["Kontonummer"] = row[1]
                        if DEBUGLEVEL > 1: print(f'# DKB #:  Kontonummer: {self.metaDic["Kontonummer"]} #')
                    # elif "Von" in row:
                    elif nrLines == 2:
                        self.metaDic["Von"] = row[1]
                        if DEBUGLEVEL > 1: print(f'# DKB #:  Von: {self.metaDic["Von"]} #')
                    # elif "Bis" in row:
                    elif nrLines == 3:
                        self.end = row[1]
                        self.metaDic["Bis"] = row[1] 
                        if DEBUGLEVEL > 1: print(f'# DKB #:  Bis: {self.metaDic["Bis"]} #')
                    # elif "Kontostand" in row:
                    elif nrLines == 4:
                        self.metaDic["Kontostand"] = row[1]
                        if DEBUGLEVEL > 1: print(f'# DKB #:  Kontostand: {self.metaDic["Kontostand"]} #')
                    elif nrLines > 6: return self.metaDic
                    nrLines +=1
           
    def _getData(self, csv_file):       
        '''
        reads the CSV file and creates data frame with the parsed data. Panda df is returned.
        https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
        ''' 
        if DEBUGLEVEL > 0: print(f"# DKB #: csv file: {csv_file} ")
        dkb_format = self._checkDkbFormat(csv_file)
        
        try:
            if dkb_format:
                df = pd.read_csv(csv_file,
                    skiprows = self.__header_line,                  
                    #encoding='utf-8', # needs to be None to be able to read German text                  
                    encoding_errors = "ignore", 
                    #warn_bad_lines=True, depricated
                    delimiter=";",
                    skipinitialspace = True,
                    parse_dates = [0,1], # to parse these colums as date
                    infer_datetime_format=True
                    )
                
                df.columns = self.__header
                return df
            else:
                return None
        except: 
            print(f"# DKB #: File not found at: {csv_file}, or file is corrupted")
            return None
        
    def _checkDkbFormat(self, csv_file) -> Any:   

        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if DEBUGLEVEL > 3: print(', '.join(row))
                # TODO: check how many columns the csv file has
                if "Kontonummer" in row:
                    if DEBUGLEVEL > 1: print('# DKB #:  DKB format csv #')
                    return True
        return False
        
