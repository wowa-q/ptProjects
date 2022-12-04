# -*- coding: iso-8859-1 -*-
'''
Created on 22.06.2021

@author: wakl8754
'''
from typing import Any
import csv
import hashlib
# import user packages
from dkb.fl.fileLoader import FileLoader
from dkb.cfg import ResponseCode as RC

DEBUGLEVEL = 3
INFO = False

class DKB(object):
    '''
    Performs parsing of the CSV file from DKB
    '''
    # the line here to find header line
                
   
    def __init__(self):
        ''' @pth input pathlib.Path type see https://docs.python.org/3/library/pathlib.html 
            pth to the folder with csv files path shall of the type pathlib.Path
        '''        
        pass
    
    def get_meta(self, csv_file):
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
        
    def _checkDkbFormat(self, csv_file) -> Any:   
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                ctr = 0
                for row in reader:
                    if DEBUGLEVEL > 4: print(', '.join(row))
                    if ctr > 7: break
                    if "Kontonummer" in row:
                        if DEBUGLEVEL > 1: print('# DKB #:  DKB format csv #')
                        konto = row[1]
                        return True                    
                    ctr =+ 1
                return False
        except FileNotFoundError:
            print(f"# DKB #: File not found at: {csv_file}, or file is corrupted")
            return False
    
    def _calculate_checksum(self, data):
        return hashlib.md5(','.join(data).encode('utf-8')).hexdigest()

    def get_lines_as_list_of_dicts(self, csv_file):
        lines = []
        dkb_dict = {}
        if self._checkDkbFormat(csv_file):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                ctr = 0
                for row in reader:
                    ctr += 1
                    if DEBUGLEVEL > 3: print(', '.join(row))
                    if ctr < 8: continue
                    dkb_dict = {}
                    
                    dkb_dict['date'] = row[0]
                    dkb_dict['booking-date'] = row[1]
                    dkb_dict['text'] = row[2]
                    dkb_dict["debitor"] = row[3]
                    dkb_dict['verwendung'] = row[4]
                    dkb_dict['konto'] = row[5]
                    dkb_dict['blz'] = row[6]
                    dkb_dict['value'] = float(row[7].replace('.','').replace(',', '.'))
                    dkb_dict['debitor-id'] = row[8]                    
                    dkb_dict['mandats_ref'] = row[9]
                    dkb_dict['customer_ref'] = row[10]
                    dkb_dict['checksum'] = hashlib.md5(','.join(row).encode('utf-8')).hexdigest()
                    lines.append(dkb_dict)                    
            if DEBUGLEVEL > 1: print(f'get_lines_as_list_of_dicts: {len(lines)}')
        return (RC.OK, lines)