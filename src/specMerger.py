#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
Created on 25.03.2021

@author: wakl8754
'''

from src.xls.XlHandler import XlRead
from src.app.fileImport import FileTreeChecker, XmlImporter


lFiles      = ['LAH.DUM.909.Q_1.6',
               'LAH.5G0.042.B_2.2',
               'LAH.DUM.857.AK_3.0F',
               'LAH.DUM.907.BF_1.4',
               'LAH.DUM.909.N_1.1',
               'LAH.DUM.909.P_1.1']
#===============================================================================
# sFileName = 'Q_LAH.DUM.857.N_2.3'
# srcPath     = 'd:/projects/001_PIA/6_xscReq/Converter/xml/'+sFileName+'.xlsx'    # path to the source specification
# trgPath     = 'd:/projects/001_PIA/6_xscReq/Converter/xml_BkUp/'+sFileName+'.xml'    # path of the target specification
# mergPath    = 'd:/projects/001_PIA/6_xscReq/Converter/merged/'+sFileName+'.xml'    # path of the merged specification
#===============================================================================

sSheet    = 'Requirements'    # name of the excel sheet, from where to read the data
trgSheet    = ''    # name of the excel sheet, to where the data need to be writen




startRow            = 4
iCustId             = 1
AffectedProduct     = 4
catExternalComments = 5
FeatureID           = 6
AnalysisStatus      = 7
anExternalComments  = 8

lValues             = []
#TODO: check this alternative: https://docs.python.org/3/library/pathlib.html
for sfl in lFiles:
    sFileName = sfl
    srcPath     = 'd:/SMG/work/specs/analysed/'+sFileName+'.xlsx'    # path to the source specification
    trgPath     = 'd:/projects/001_PIA/6_xscReq/Converter/xml_BkUp/'+sFileName+'.xml'    # path of the target specification
    mergPath    = 'd:/projects/001_PIA/6_xscReq/Converter/merged/'+sFileName+'.xml'    # path of the merged specification
    srcSpec     = XlRead(srcPath)
    trgSpec     = XmlImporter(trgPath) #XlRead(trgPath)
    
    bSrcSheet           = srcSpec.openSheet(sSheet)     
    
    if bSrcSheet:
        endRow      = srcSpec.lastRow
        endCol      = srcSpec.lastColumn
        
        for iRow in range(startRow, endRow+1):   
            lValues.append({'CustId'                :srcSpec.getCellContant(iRow, iCustId),
                            'AffectedProduct'       :srcSpec.getCellContant(iRow, AffectedProduct),
                            'ResponsibleBundle'     : '',
                            'catExternalComments'   :srcSpec.getCellContant(iRow, catExternalComments),
                            'FeatureID'             :srcSpec.getCellContant(iRow, FeatureID),
                            'AnalysisStatus'        :srcSpec.getCellContant(iRow, AnalysisStatus),
                            'anExternalComments'    :srcSpec.getCellContant(iRow, anExternalComments)
                            })
    else:
        print('scrSheet does not exist')    
        
    for val in lValues:
        req=trgSpec.findReq(val['CustId'])
        if req != None: 
            #print(trgSpec.getCategContant(req, 'AffectedProduct'))            
            #print('updating req: ', req.find('General').find('CustId').text)       
            if val['AffectedProduct'] == 'Informational':            
                trgSpec.updateCategProduct(req, 'Informational')            
                trgSpec.updateCategStatus(req, 'Done')
                
            elif val['AffectedProduct'] == 'Project':
                trgSpec.updateCategProduct(req, 'Project')
                trgSpec.updateCategBundle(req, 'Project')
                trgSpec.updateCategStatus(req, 'Done')
                
            elif val['AffectedProduct'] == 'tresos': 
                trgSpec.updateCategProduct(req, 'tresos')
                if trgSpec.getCategContant(req, 'ResponsibleBundle') != None:
                    # the responsible bundle is already set in original spec. -> do not change
                    print(trgSpec.getCategContant(req, 'ResponsibleBundle')) 
                    
                else:
                    # the responsible bundle is NOT set in target spec.
                    if val['ResponsibleBundle'] != None or val['ResponsibleBundle'] != '':
                        # set the responsible bundle from Nikos spec. if it was set there
                        trgSpec.updateCategBundle(req, val['ResponsibleBundle'])
                        trgSpec.updateCategStatus(req, 'Done')
                    else:
                        # responsible bundle not set in both specs.
                        trgSpec.updateCategComment(req, 'wakl: set responsible bundle')
                        trgSpec.updateCategStatus(req, 'Open')
                
                if val['AnalysisStatus'] == None or val['AnalysisStatus'] == '':
                    # analysis status set in Nikos spec. -> take over
                    trgSpec.updateTresosStatus(req, val['AnalysisStatus'])
                else:
                    # do nothing
                    
                    pass
        else: 
            print('Could not find Requirement with ID: ', val['CustId'])
            
            
    trgSpec.save(name=mergPath)   
    

if __name__ == '__main__':
    pass