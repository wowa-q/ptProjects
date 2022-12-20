# -*- coding: iso-8859-1 -*-
'''
Created on 22.06.2021

@author: wakl8754
'''
# standard libraries
import csv
import hashlib
from typing import Any
# 3rd party libraries

# user packages
from dkb.cfg import ResponseCode as RC

DEBUGLEVEL = 3
INFO = False

class Dkb():
    """ Performs parsing of the CSV file from DKB """
    def __init__(self):
        ''' @pth input pathlib.Path type see https://docs.python.org/3/library/pathlib.html 
            pth to the folder with csv files path shall of the type pathlib.Path
        '''
        self.end        = ''
        self.meta_dict = {
                "Kontonummer" : "",
                "Von" : "",
                "Bis" : "",
                "Kontostand" : ""
            }
    
    def get_meta(self, csv_file):
        ''' get the meta data from the csv file '''
        dkb_format = self._check_dkb_format(csv_file)
        if dkb_format:            
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                nr_lines = 0
                for row in reader:
                    # if "Kontonummer" in row:
                    if nr_lines == 0:
                        self.meta_dict["Kontonummer"] = row[1]
                        if DEBUGLEVEL > 1: 
                            print(f'# DKB #:  Kontonummer: {self.meta_dict["Kontonummer"]} #')
                    # elif "Von" in row:
                    elif nr_lines == 2:
                        self.meta_dict["Von"] = row[1]
                        if DEBUGLEVEL > 1: 
                            print(f'# DKB #:  Von: {self.meta_dict["Von"]} #')
                    # elif "Bis" in row:
                    elif nr_lines == 3:
                        self.end = row[1]
                        self.meta_dict["Bis"] = row[1] 
                        if DEBUGLEVEL > 1: 
                            print(f'# DKB #:  Bis: {self.meta_dict["Bis"]} #')
                    # elif "Kontostand" in row:
                    elif nr_lines == 4:
                        self.meta_dict["Kontostand"] = row[1]
                        if DEBUGLEVEL > 1: 
                            print(f'# DKB #:  Kontostand: {self.meta_dict["Kontostand"]} #')
                    elif nr_lines > 6: 
                        break
                    nr_lines +=1
            return self.meta_dict
        return None

    @staticmethod
    def _check_dkb_format(csv_file) -> Any:   
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                ctr = 0
                for row in reader:
                    if DEBUGLEVEL > 4: 
                        print(', '.join(row))
                    if ctr > 7: 
                        break
                    if "Kontonummer" in row:
                        if DEBUGLEVEL > 1: 
                            print('# DKB #:  DKB format csv #')
                        # konto = row[1]
                        return True                    
                    ctr =+ 1
                return False
        except FileNotFoundError:
            print(f"# DKB #: File not found at: {csv_file}, or file is corrupted")
            return False
    
    @staticmethod
    def _calculate_checksum(data):
        return hashlib.md5(','.join(data).encode('utf-8')).hexdigest()

    def get_lines_as_list_of_dicts(self, csv_file):
        ''' get the line from csv file and return as a dict packed in a list of lines'''
        lines = []
        dkb_dict = {}
        if self._check_dkb_format(csv_file):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                ctr = 0
                for row in reader:
                    ctr += 1
                    if DEBUGLEVEL > 3: 
                        print(', '.join(row))
                    if ctr < 8: 
                        continue
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
            if DEBUGLEVEL > 1: 
                print(f'get_lines_as_list_of_dicts: {len(lines)}')
        return (RC.OK, lines)