'''
Created on 30.03.2021

@author: wakl8754
'''

from src.xls.XlHandler import XlRead
from src.app.fileImport import XmlImporter
from src.acaf.Interpreter import AcafInterpreter

srcPath = 'd:/SMG/work/specs/acaf/'
trgPath = 'D:/projects/001_PIA/6_xscReq/xsc_BundleCReq_VWAG/doc/project/requirements/analysis/Step2/xml/'
mrgPath = 'd:/SMG/work/specs/merged/acaf/'
specs = {'020_027_LAH.DUM.909.G_Unified_Diag_Serv_Prot_V2.8.1_classification':'LAH.DUM.909.G_2.8.1',
         '020_109_LAH.DUM.909.A_80114_nonOBD_V5.8_classification':'LAH.DUM.909.A_5.8',
        # '030_043_LAH.DUM.857.AN_ZentraleAktNetzwerkdiag_V3.0F_classification':'LAH.DUM.857.AN.1_3.0F',
         '030_055_LAH.DUM.857.AK_KonzernLAH_NM_high_.V3.0F_classification':'LAH.DUM.857.AK_3.0F',
         '030_184_LAH.000.900.AE_IP-Kommunikation_V1.6_classification':'LAH.000.900.AE_1.6',
         '030_186_LAH.000.900.AD_Ethernet_100Base_T1_V1.11_classification':'LAH.000.900.AD_1.11',
         '030_193_LAH.DUM.900.T_Ethernet1000Base_T1_V1.3_classification':'LAH.DUM.900.T_1.3',
         '030_196_LAH.DUM.909.N_IP_Signalkommunikation_V1.1_classification':'LAH.DUM.909.N_1.1',
         '030_197_LAH.DUM.909.P_IP_Network_Management_V1.2_classification':'LAH.DUM.909.P_1.2',
         '030_198_LAH.DUM.909.Q_SOME_IP_Anwendungsspezifikation_V1.7_classification':'LAH.DUM.909.Q_1.7',
         '030_210_LAH.000.900.AS_Zeitsynchronisation_ueber_Ethernet_V1.1_classification':'LAH.000.900.AS_1.1',
         '030_211_LAH.DUM.10A.909_Service_Discovery_V1.3_classification':'LAH.DUM.10A.909_1.3',
         '030_230_LAH.000.036.D_Zeitsynchronisation_CAN_V1.4_classification':'LAH.000.036.D_1.4',}

keys        = specs.keys()
sSheet      = 'Tabelle1'

for spec in keys:
    print(spec)
    print(specs[spec])
    srcSpec     = srcPath+spec+'.xlsx'    # path to the source specification
    trgSpec     = trgPath+specs[spec]+'.xml'    # path of the target specification
    mrgSpec     = mrgPath+specs[spec]+'.xml'    # path of the merged specification
    
    acafSpec    = XlRead(srcSpec)
    ebSpec      = XmlImporter(trgSpec)
    acafSheet   = acafSpec.openSheet(sSheet)

    if acafSheet != None:
        parser = AcafInterpreter(acafSpec, ebSpec)
        print(parser._checkIdCol())
        print(parser._checkRelevanceCol())
        print(parser._checkClassCol())
        print(parser._checkAffectedElement())
        print(parser._checkTypCol())
        print(parser._checkCommentCol())
        print(        parser.reader.lastRow)
#         while parser.readLine():
#             print(parser.currentLine)
#             parser.currentLine = parser.currentLine+1
#             xlsReq=parser.readLine()
#             if parser.checkIsRequirement(xlsReq['type']): 
#                 print('# REQUIREMENT #')           
#                 if parser.checkRelevance(xlsReq['relevance']):
#                     print('# RELEVANT #')
#                     t = parser.getTarget(xlsReq['target'])
#                     if t == 'tresos':
#                         print('# TRESOS #')
#                         parser.setTresos(xlsReq['id'], xlsReq['rationale'])
#                     elif t == 'Project':
#                         print('# PROJECT #')
#                         parser.setProject(xlsReq['id'], xlsReq['rationale'])
#                     else:
#                         print('unknown target')
#                 else:
#                     print('# INFO #')
#                     parser.setInfo(xlsReq['id'], xlsReq['rationale'])
#             else:
#                 parser.setInfo(xlsReq['id'], 'acaf: not a requirement')
#          
#         else:
#             print (srcSpec + 'does not have sheet with the name: ' + sSheet)
#             
    
        parser.saveXml(mrgSpec)
    
if __name__ == '__main__':
    pass