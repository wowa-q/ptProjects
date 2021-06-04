'''
Created on 28.01.2021

@author: wakl8754
'''
from src.app.rif import RIF
from src.app.fileImport import XmlImporter

class Regelwerk():
    xmlData = 'XML-Data: -'
    def __init__(self, param):
        print('get xml data')
        xmlData = 'XML-Data: Super'
        
class R1(RIF, Regelwerk): 
    '''
        noReq > noACGReq
    '''
    def __init__(self):
        #self.xmlData = super.xmlData
        super().__init__('xml')
        print(super().xmlData)
        
    def verify(self):
        print('verify R1')
    def result(self):
        print('result R1')
        
class R2(RIF):
    def __init__(self):
        pass
    
    def result(self):
        print('result R2') 
    def verify(self):
        print('verify R2')
    
    