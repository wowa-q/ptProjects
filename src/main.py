'''
Created on 28.01.2021

@author: wakl8754
'''
#------------------------------------------------------------------------------ 
from src.app.fileImport import FileTreeChecker, XmlImporter
from src.app.regelwerk import *
#------------------------------------------------------------------------------ 
rootpath = "D:/projects/910_prProjects/valReq"
specrootpath = 'd:/SMG/work/specs/QLAH_E3_Nov 2020_V32_PDF'

myPath = rootpath + "/statusreport"
def getSpecName(fList):
    specName = []
    for f in fList:        
        if f.find("QLAH")>0:
            f=f[f.find("QLAH")+5:]   
        f=f[f.find("LAH"):]
        shortNmEnd=f.find("_")
        shortName=f[:f.find("_")]
        specName.append([f, shortName, f[shortNmEnd+1:-4]])
    return specName 
specs=[]
bundles = ["/000_Allgemein", 
           "/020_Diagnose", 
           "/030_Vernetzung", 
           "/040_Transportprotokolle", 
           "/050_Software", 
           "/060_Mechatronik", 
           "/070_Systemsicherheit", 
           "/080_Security", 
           "/090_Beleuchtung", 
           "/110_Energiemanagement", 
           "/120_MFL", 
           "/130_Klemm- und Startersteuerung", 
           "/140_Bordnetz"]

for bundle in bundles:
    print(bundle + '  ')
    specpath = specrootpath + bundle    
    print(specpath)
    ftc=FileTreeChecker(specpath)
    specs.append(getSpecName(ftc.fList))
    
#ftc=FileTreeChecker(myPath)

#ftc.getPrjectFiles()

 
  

try:
    f=open("specs.txt", "w")
except:
    print('file already exists')
print(specs)
for bundle in specs:
    for spec in bundle:
        print(spec[0])
        print(spec[1])
        f.write(spec[0])
        f.write("\t")
        f.write(spec[1])
        f.write("\t")
        f.write(spec[2])
        f.write("\n")
f.close()

xmlt=XmlImporter(myPath+"/VWAG_Baseline_Status_Report.xml")
xmlt.setBaseline('2020_05_E3')
xmlt.getDocNr()

'''
print(xmlt.nrOfDocs)

regelwerk = Regelwerk('xml')

r1 = R1()
r2 = R2()
for r in [r1, r2]:
    r.verify()
    r.result()
'''
    
if __name__ == '__main__':
    pass