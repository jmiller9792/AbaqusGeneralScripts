from abaqus import *
from abaqusConstants import *
ModelList = ['B1_1_RibNoTow', 'B1_2_NoRibNoTow', 'B1_3_MetalThick',\
             'B2_1_BotCF', 'B3_1_TopCF', 'B4_1_BothClosed', 'B4_2_BothOpen']
for model_name in ModelList:
#model_name='B1_1_RibNoTow'
	print('C:/aFiles/Abaqus2017WDir/FordTowStudy3/'+model_name+'.odb')
	session.viewports['Viewport: 1'].setValues(displayedObject=None)
	o1 = session.openOdb(name='C:/aFiles/Abaqus2017WDir/FordTowStudy3/'+model_name+'.odb')
	session.viewports['Viewport: 1'].setValues(displayedObject=o1)
	odb = session.odbs['C:/aFiles/Abaqus2017WDir/FordTowStudy3/'+model_name+'.odb']
	session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
		NODAL), ('UR', NODAL), ), nodeSets=('ENDCONTROLPT', ))
	x0 = session.xyDataObjects['U:Magnitude PI: ASSEMBLY N: 2']
	x1 = session.xyDataObjects['U:U1 PI: ASSEMBLY N: 2']
	x2 = session.xyDataObjects['U:U2 PI: ASSEMBLY N: 2']
	x3 = session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
	x4 = session.xyDataObjects['UR:Magnitude PI: ASSEMBLY N: 2']
	x5 = session.xyDataObjects['UR:UR1 PI: ASSEMBLY N: 2']
	x6 = session.xyDataObjects['UR:UR2 PI: ASSEMBLY N: 2']
	x7 = session.xyDataObjects['UR:UR3 PI: ASSEMBLY N: 2']
	session.writeXYReport(fileName=model_name+'.rpt', appendMode=OFF, xyData=(x0, x1, x2, x3, x4, x5, 
		x6, x7))
	del session.xyDataObjects['U:Magnitude PI: ASSEMBLY N: 2']
	del session.xyDataObjects['U:U1 PI: ASSEMBLY N: 2']
	del session.xyDataObjects['U:U2 PI: ASSEMBLY N: 2']
	del session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
	del session.xyDataObjects['UR:Magnitude PI: ASSEMBLY N: 2']
	del session.xyDataObjects['UR:UR1 PI: ASSEMBLY N: 2']
	del session.xyDataObjects['UR:UR2 PI: ASSEMBLY N: 2']
	del session.xyDataObjects['UR:UR3 PI: ASSEMBLY N: 2']