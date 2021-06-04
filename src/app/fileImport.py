#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''

Created on 12.12.2020

@author: wakl8754
#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
import xml.etree.ElementTree as et
import codecs               # to convert the german letters
import posixpath as posix
import os as os
#TODO: check this alternative: https://docs.python.org/3/library/pathlib.html
class FileTreeChecker(object):
    '''
    classdocs
    '''
    def __init__(self, observedPath):
        '''
        @param: Path string which to be observed 
            observedPath  
        '''  
        try:      
            self.fList=os.listdir(observedPath) # the path shall be verified before instantiate
        except:
            print('Folder not found')
            self.fList=None
        
        self._prFiles = []
        self._verifiedpath = ''
    
    def getPrjectFiles(self):
        if len(self._prFiles) == 0:
            self._getFiles('xml')
        else:
            # TODO: created for testing if condition - can be removed
            return []
        return self._prFiles
    
    def _getFiles(self, ftype):
        for f in self.fList:
            if ftype in f and ftype == 'xml':
                self._prFiles.append(f)

REQUIREMENTS    = 1
REQUIREMENT     = 0
GENERAL         = 0
CATEGORIZATION  = 1
CUSTID          = 0
PRODUCT         = 0
BUNDLE          = 1
CATSTATUS       = 3

class XmlImporter(object):
    '''
    @brief: xml parser
        takes the file path to the xml file and ..
    @reference: 
        https://docs.python.org/3/library/xml.etree.elementtree.html
        https://www.edureka.co/blog/python-xml-parser-tutorial/
    '''

    def __init__(self, xmlPath):
        '''
        Constructor
        '''      
        self.topchilds=[]   # top level xml child list
        #=======================================================================
        # check if the file path exists at all
        #=======================================================================
        if posix.exists(xmlPath):
            pass
        else:            
            raise BaseException('file not found %s', xmlPath)
        
        self.myTree=et.parse(xmlPath)
        self.myRoot=self.myTree.getroot()
        
        for child in self.myRoot:
            self.topchilds.append(child)
    def save(self, name='test.xml'):
        self.myTree.write(name)
    
    def findReq(self, sId):
        for req in self.myRoot.iter('Requirement'):
            if sId == req.find('General').find('CustId').text:
                return req
        return None
    
    def getCategContant(self, req, sTagName):
        # return the requested value
        try:
            return req.find('TresosCategorization').find(sTagName).text
        except:
            return None
        
    def getTresosContant(self, req, sTagName):
        # return the requested value
        try:
            return req.find('TresosACG').find(sTagName).text
        except:
            return None
        
    def updateCategProduct(self, req, sVal):
        if req != None:
            self._checkExisting(req, 'TresosCategorization')
            try:
                req.find('TresosCategorization').find('AffectedProduct').text = sVal
            except:
                el = self.create('AffectedProduct')
                el.text = sVal
                req.find('TresosCategorization').append(el)
    
    def updateCategBundle(self, req, sVal):
        if req != None:
            self._checkExisting(req, 'TresosCategorization')
            try:
                req.find('TresosCategorization').find('ResponsibleBundle').text = sVal
            except:
                el = self.create('ResponsibleBundle')
                el.text = sVal
                req.find('TresosCategorization').append(el)
    
    def updateCategStatus(self, req, sVal):
        if req != None:
            self._checkExisting(req, 'TresosCategorization')
            try:
                req.find('TresosCategorization').find('CategorizationStatus').text = sVal
            except:
                el = self.create('CategorizationStatus')
                el.text = sVal
                req.find('TresosCategorization').append(el)
    def updateCategComment(self, req, sVal):
        if req != None:
            self._checkExisting(req, 'TresosCategorization')
            try:
                req.find('TresosCategorization').find('InternalComments').text = sVal
            except:
                el = self.create('InternalComments')
                el.text = sVal
                req.find('TresosCategorization').append(el)
                          
    def updateTresosStatus(self, req, sVal):
        if req != None:
            self._checkExisting(req, 'TresosACG')
            try:
                req.find('TresosACG').find('AnalysisStatus').text = sVal
            except:
                el = self.create('AnalysisStatus')
                el.text = sVal
                req.find('TresosACG').append(el)
    
    def updateTresosComment(self, req, sVal):
        
        if req != None:
            self._checkExisting(req, 'TresosACG')
            try:
                req.find('TresosACG').find('Comments').text = sVal
            except:
                el = self.create('Comments')
                el.text = sVal
                req.find('TresosACG').append(el)
                
    def getNumberOfReq(self):
        nr = 0
        for x in self.myRoot.iter('Requirement'):
            nr=nr+1            
        print('Number of requirements: ', nr)
        return nr
    
    def _checkExisting(self, req, sName):
        #sName:TresosACG
        if req.find(sName) != None:
            return
        else:
            el = self.create(sName)
            req.append(el)
            
    def create(self,sName):        
        print('create ', sName)
        return et.Element(sName)
        
    #------------------------------------------------------------------------------                 
    
    def setBaseline(self, baseline):        
        self.basline = None
        for child in self.topchilds:            
            if child.tag=='BaseLine' and child.attrib['name'] == baseline:
                self.basline = child
                break;
        if self.basline == None:
            raise('Baseline not found')
    
    def getDocNr(self):    
        self.docsList = []
        try:
            for sub in self.basline:
                self.docsList.append(sub)
            self.nrOfDocs = len(self.docsList)
        except:
            raise('no baseline selected')
        
    
    