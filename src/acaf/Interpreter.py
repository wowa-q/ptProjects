'''
Created on 29.03.2021

@author: wakl8754
'''

class AcafInterpreter(object):
    '''
    classdocs
    '''


    def __init__(self, xlsSheetReader, xmlSpec):
        '''
        Constructor
        '''
        self.reader         = xlsSheetReader
        self.spec           = xmlSpec
        self.currentLine    = 1
        
    def colNumbers(self):
        col = 1
        while col < self.reader.lastRow:
            print(self.reader.getCellContant(1, col))
            col = col+1
            
        
    def readLine(self):
        #FIXME: Endlos loop
        ID          = self._checkIdCol()  #1
        TYP         = self._checkTypCol() #4
        RELEVANCE   = self._checkRelevanceCol() # 6
        TARGET      = self._checkTargetCol()
        CLASS       = self._checkClassCol()
        RATIONALE   = self._checkCommentCol()
        print(self.reader.getCellContant(self.currentLine, ID))
        print(self.reader.getCellContant(self.currentLine, TYP))
        return {'id'            : self.reader.getCellContant(self.currentLine, ID),
                'type'          : self.reader.getCellContant(self.currentLine, TYP),
                'relevance'     : self.reader.getCellContant(self.currentLine, RELEVANCE),
                'target'        : self.reader.getCellContant(self.currentLine, TARGET),
                'classification': self.reader.getCellContant(self.currentLine, CLASS),
                'rationale'     : 'acaf: ' + self.reader.getCellContant(self.currentLine, RATIONALE)}
        
        if self.currentLine < self.reader.lastRow:
            self.currentLine = self.currentLine+1
        else:
            return False
    
    def checkIsRequirement(self, typ):
        if 'Anforderung' in typ:
            return True
        else:
            return False

    def checkRelevance(self, relevance):
        if relevance == 'Potentially relevant':
            return True
        else:
            return False
        
    def _checkAffectedElement(self):
        for cl in range(1,20):
            if 'Affected elements' in self.reader.getCellContant(1, cl):
                return cl
            else:
                return 0
        
    
        
            
    def _getClNumber(self, sName):       
        for cl in range(1,20):
            #print(sName)
            #print(self.reader.getCellContant(1, cl))
            if sName in self.reader.getCellContant(1, cl) :
                return cl
            
        return 0
    
    def _checkIdCol(self):
        return self._getClNumber('Object ID')  or self._getClNumber('ID')
                    
    def _checkTypCol(self):
        return self._getClNumber('Typ')
    
    def _checkRelevanceCol(self):
        return self._getClNumber('Relevance')
    
    def _checkTargetCol(self):
        return self._getClNumber('Target')
    
    def _checkClassCol(self):
        return self._getClNumber('Classification')
    
    def _checkCommentCol(self):
        return self._getClNumber('Internal comment')
    

    
    
    
    def getTarget(self, target):
        if target == 'BSW' or target == 'Platform Configuration':
            return 'tresos'
        elif target in ['Platform Extension', 'Reference Application', 'Framework Library', 'Generator']:
            return 'Project'
    
    def setTresos(self, sID, rational=None):
        req=self.spec.findReq(sID)
        if req != None:
            self.spec.updateCategProduct(req, 'tresos')
            if rational != None:
                self.spec.updateCategComment(req, rational)
            return True
        else:
            return False
        
    def setProject(self, sID, rational=None):
        req=self.spec.findReq(sID)
        if req != None:
            self.spec.updateCategProduct(req, 'Project')
            self.spec.updateCategBundle(req, 'Project')
            self.spec.updateCategStatus(req, 'Done')
            if rational != None:
                self.spec.updateCategComment(req, rational)
            return True
        else:
            return False
    
    def setInfo(self, sID, rational=None):
        req=self.spec.findReq(sID)
        if req != None:
            self.spec.updateCategProduct(req, 'Informational')            
            self.spec.updateCategStatus(req, 'Done')
            if rational != None:
                self.spec.updateCategComment(req, rational)
            return True
        else:
            return False
    
    def saveXml(self, name='unnamed.xml'):
        self.spec.save(name=name)
    

    
    
    #===========================================================================
    # internal
    #===========================================================================
    
    def __repr__(self):
        #TODO: update
        return f"AcafInterpreter('{self.reader}', '{self.spec}', '{self.currentLine}')"
        