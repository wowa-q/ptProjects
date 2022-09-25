#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#import codecs               # to convert the german letters
#from pathlib import Path
from typing import List    # https://docs.python.org/3/library/pathlib.html

REQUIREMENTS    = 1
REQUIREMENT     = 0
GENERAL         = 0
CATEGORIZATION  = 1
CUSTID          = 0
PRODUCT         = 0
BUNDLE          = 1
CATSTATUS       = 3

class FileLoader():
    ''' class to handle input files '''
    def __init__(self, pth) -> None:
        ''' @pth input Path type see https://docs.python.org/3/library/pathlib.html '''
        # if pth.is_dir(): self.path = pth
        self.path = pth
        self.fileList = []
    
    def _createFileList(self) -> List:
        ''' creates a list of csv files in the given folder '''
        try:
            self.fileList=list(self.path.glob('**/*.csv')) # listing all csv files in the directory tree
        except:
            print('f, Folder not found:', self.path)
        if len(self.fileList) == 0:
            print(f"No csv files in {self.path}")
        return self.fileList

    def getCsvFilesList(self) -> List:
        return self._createFileList()
        