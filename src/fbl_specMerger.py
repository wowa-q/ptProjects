#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
Created on 25.03.2021

@author: wakl8754
'''

import logging

from src.app.fileImport import FileTreeChecker
from src.xls.XlHandler import XlRead


logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

waklFileName = 'Q_LAH80126-wakl'
solFileName = 'Q_LAH80126-sol'
mergedFileName = 'Q_LAH80126-merged'
srcPath = 'D:/SMG/work/FBL/' + waklFileName + \
    '.xlsx'    # path to the source specification
waklPath = 'd:/SMG/work/FBL/' + solFileName + \
    '.xlsx'   # path of the target specification
mergPath = 'd:/SMG/work/FBL/' + mergedFileName + \
    '.xlsx'    # path of the merged specification
waklSpec = XlRead(srcPath)
solSpec = XlRead(waklPath)
#mrgSpec = XlRead(mergPath)


def getSolValues(solSpec):
    print('# start: getSolValues')
    startRow = 7
    iCustId = 1
    iTarget = 10
    iPrio = 11
    sSheet = 'Matrix'    # name of the excel sheet, from where to read the data
    bSrcSheet = solSpec.openSheet(sSheet)
    lValues = []
    if bSrcSheet:
        endRow = solSpec.lastRow
        endCol = solSpec.lastColumn
        logging.debug(solSpec)
        for iRow in range(startRow, endRow + 1):

            if solSpec.getCellContant(iRow, iTarget) or solSpec.getCellContant(iRow, iPrio):
                lValues.append({'CustId': solSpec.getCellContant(iRow, iCustId),
                                'target': solSpec.getCellContant(iRow, iTarget),
                                'prio': solSpec.getCellContant(iRow, iPrio)
                                })
    else:
        print('scrSheet does not exist')
        return None
    return lValues


def getWaklValues(waklSpec):
    print('# start: getWaklValues')
    startRow = 7
    iTarget = 13
    iPrio = 14
    sSheet = 'Matrix'    # name of the excel sheet, from where to read the data
    bSrcSheet = waklSpec.openSheet(sSheet)
    lSolValues = getSolValues(solSpec)

    if bSrcSheet:
        logging.debug('waklSpec work sheet opened')
        for di in lSolValues:
            row = waklSpec.searchRow(sValue=di['CustId'], iStart=startRow)
            if row != None:
                waklSpec.writeCell(row, iTarget, sValue=di['target'])
                waklSpec.writeCell(row, iPrio, sValue=di['prio'])

#         endRow = waklSpec.lastRow
#         endCol = waklSpec.lastColumn
#         for iRow in range(startRow, endRow + 1):
#             logging.debug(waklSpec)
#             sId = waklSpec.getCellContant(iRow, iCustId)
#             for di in lSolValues:
#                 if sId in di['CustId']:
#                     pass
#                     # print(di)


if __name__ == '__main__':
    getWaklValues(waklSpec)
    waklSpec.save()
