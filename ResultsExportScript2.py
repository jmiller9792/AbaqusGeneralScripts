from abaqus import *
from abaqusConstants import *
# execfile('C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\PostProcessing\\ResultsExportScript2.py')

## MODIFY THESE!!!
#currentModel='C:\\aaResearch\\aFordHM\\SS3_v1\\pre\\ConvergenceStudy_7May\\SS3_Convergence.cae'
# currentModel='C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\ForkConcept_2019-10-30.cae'
ODB_path = 'C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\'
massPropFile = 'LCF_2019-11-25.csv'
myoutfile = open(massPropFile,'w+')

# If model is not open already, open currentMode
# if mdb.pathName!=currentModel:
    # mdb = openMdb(pathName=currentModel)
               


#ODBs will be exported to new location as backup
#UpgradedODB_path = 'C:/aFiles/Abaqus2018WDir/SectionStudy3/'


for model in mdb.models.values():

    #Print Model Name and path (original)
    origPath = ODB_path+model.name+'.odb'
    print('Reading: '+origPath)
    
    # if upgradeRqd
        # upPath = UpgradedODB_path+model.name+'_2018.odb'
        # print('Moving to: '+upPath)
        
        # #Upgrade to Abaqus 2018 and move location
        # session.upgradeOdb(origPath,upPath, )
    
    # Set Objects and open in viewport
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    # o1 = session.openOdb(name=upPath)
    o1 = session.openOdb(name=origPath)
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    # odb = session.odbs[upPath]
    odb = session.odbs[origPath]
    
    # # Extract Data Lists
    session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
        NODAL), ), nodeSets=("REFNODE_AXLECENTER", "REFNODE_BAREND", 
        "REFNODE_WHEELCONTACT", ))
    x0 = session.xyDataObjects['U:U1 PI: HANDLEBAR-1 N: 3']
    x1 = session.xyDataObjects['U:U1 PI: WHEELFIXTURE-2 N: 1']
    x2 = session.xyDataObjects['U:U3 PI: WHEELFIXTURE-2 N: 4']
    session.writeXYReport(fileName=model.name+'.rpt',appendMode=OFF, xyData=(x0, x1, x2))
    
    
    #I don't know why the following works.   HAd issuse previously with it not updating which model the mass properties came from
    nam = model.name
    print(nam)
    a = mdb.models[nam].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a.regenerate()
    mass = a.getMassProperties()['mass']
    print 'Mass = ', mass
    myoutfile.write(model.name)
    myoutfile.write(",")
    myoutfile.write(str(mass))
    
    # x1 = U:U1 PI: WHEELFIXTURE-2 N: 1
    loadCaseNumber = 1 #Load case number for fore-aft
    foreAftDisp = x1.data[loadCaseNumber-1][1] #second index [1] is y value, first[0] is x value
    myoutfile.write(",")
    myoutfile.write(str(foreAftDisp))
    
    loadCaseNumber = 2 #Load case number for lat2.0
    latDisp = x2.data[loadCaseNumber-1][1] #second index [1] is y value, first[0] is x value
    myoutfile.write(",")
    myoutfile.write(str(latDisp))
    
    loadCaseNumber = 3 #Load case number for torsion
    torsionDisp = x0.data[loadCaseNumber-1][1] #second index is y value, first is x value
    myoutfile.write(",")
    myoutfile.write(str(torsionDisp))
    

    # myoutfile.write(",")
    # myoutfile.write(str(mass))
    # myoutfile.write(",")
    # myoutfile.write(str(mass))
    myoutfile.write("\n")

    del session.xyDataObjects['U:U1 PI: HANDLEBAR-1 N: 3']
    del session.xyDataObjects['U:U1 PI: WHEELFIXTURE-2 N: 1']
    del session.xyDataObjects['U:U3 PI: WHEELFIXTURE-2 N: 4']



myoutfile.close()