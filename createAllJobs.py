from abaqus import *
from abaqusConstants import *
#execfile('C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\PostProcessing\\createAllJobs.py')

## NOTE: Current implementation works on current open model.  
# currentModel='C:\\awdir\\abq2018hf1wdir\\sbc_lcf\\ForkConcept_2019-10-30.cae'
## If model is not open already, open currentMode
# if mdb.pathName!=currentModel:
	# mdb = openMdb(pathName=currentModel)
	
for model in mdb.models.values():
	

	mdb.Job(name=model.name, model=model.name, description='', 
		type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
		memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
		scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
		numDomains=4, numGPUs=0)