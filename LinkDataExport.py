from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

# execfile('C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\PostProcessing\\ResultsExportScript2.py')
# execfile('C:\\awdir\\abq2019hf2wdir\\wavinessLink\\LinkDataExport.py')
ODB_path = 'C:\\awdir\\abq2019hf2wdir\\wavinessLink\\'

# partName = 

#resultsFiles = ['k02-5','k02-20']
resultsFiles = ['k02-10b2-prop1']
for modelName in resultsFiles:

    #Print Model Name and path (original)
	origPath = ODB_path+modelName+'.odb'
	print('Reading: '+origPath)



	# o3 = session.openOdb(name='C:/awdir/abq2019hf2wdir/wavinessLink/d02.odb')
	o3 = session.openOdb(name=origPath)
	session.viewports['Viewport: 1'].setValues(displayedObject=o3)
	session.viewports['Viewport: 1'].makeCurrent()
	# a = mdb.models['b01-Meshing2'].rootAssembly
	# session.viewports['Viewport: 1'].setValues(displayedObject=a)
	# session.viewports['Viewport: 1'].setValues(
		# displayedObject=session.odbs['C:/awdir/abq2019hf2wdir/wavinessLink/d02.odb'])
	# session.viewports['Viewport: 1'].assemblyDisplay.setValues(
		# optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)

	odb = session.odbs[origPath]
	session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF', 
		NODAL, ((COMPONENT, 'RF3'), )), ), nodeSets=("FIXEDPOINT", ))
	x0 = session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 1']
	# session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
		# NODAL, ((COMPONENT, 'U3'), )), ), 
		# nodeSets=("LOADPOINT", ))
	session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
		NODAL, ((COMPONENT, 'U3'), )), ), nodeSets=("LOADPOINT", ))
	x1 = session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
	
	session.writeXYReport(fileName=modelName+'.rpt', appendMode=OFF, xyData=(x0, x1))	

	del	session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 1']
	del session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
	
# session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF', 
	# NODAL, ((COMPONENT, 'RF3'), )), ('U', NODAL, ((COMPONENT, 'U3'), )), ), 
	# nodeSets=("LOADPOINT", ))