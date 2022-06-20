from abaqus import *
from abaqusConstants import *
# from scipy import spatial
# execfile('C:/awdir/abq2019hf2wdir/wavinessLink/orientMapV3_sectionbased.py')

#Checks:
#   -ensure parts are meshed
#   -check file path

# Name initialization
modelName = 'k02-10b2-2W-prop'
wirePart = 'linkWire' #Meshed beforehand
solidPart = 'V7-11_FEA_Q96-2'
sectionNumber = 0 # numbered position in section list (starting from zero)

class OrientationData:
    # Class used for data storage and association
    def __init__(self,label,centroid,orientationPoints):
        self.label = label
        self.centroid = centroid
        self.orient = orientationPoints
        self.solidElements = []
def centroid(selement, sp):  #arbitrary 3d element object and part object
    #Function to calculate center of element by averaging coordinates in each dimension
    xtot = 0
    ytot = 0
    ztot = 0
    numNodes = len(selement.connectivity)
    for snodeind in selement.connectivity:
        xtot = sp.nodes[snodeind].coordinates[0]+xtot
        ytot = sp.nodes[snodeind].coordinates[1]+ytot
        ztot = sp.nodes[snodeind].coordinates[2]+ztot
    centroid = (xtot/numNodes,ytot/numNodes,ztot/numNodes)
    return centroid

def distance(pt1, pt2):
    #compute distance between two 3d points
    x1 = pt1[0]
    x2 = pt2[0]
    y1 = pt1[1]
    y2 = pt2[1]
    z1 = pt1[2]
    z2 = pt2[2]
    a = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
    return  a ** 0.5

#initialize wire part (wp) and solid part (sp) objects
wp = mdb.models[modelName].parts[wirePart]
sp = mdb.models[modelName].parts[solidPart]
sp_towSet = sp.sectionAssignments[sectionNumber].getSet()
#sp_towSet = mdb.models[modelName].parts[solidPart].sectionAssignments[secNum].getSet()



### For wire part, determine orientations of each element
# Create list of orientation reference points and corresponding orientation points for assigning rectangular orientations
numOrientations = len(wp.elements)
# Initialize orientation variable lists
orientList = [0]*numOrientations
orientCenters = [0]*numOrientations
# for each element in the wire part, determine orientation points and centroids

for element in wp.elements:

    startNodeIndex = element.connectivity[0] # reported in node index rather than label
    endNodeIndex = element.connectivity[1]# reported in node index rather than label
    orientC = wp.nodes[startNodeIndex].coordinates #origin
    orientA = wp.nodes[endNodeIndex].coordinates # x' direction

    if (orientC[1]-orientA[1]==0)and(orientC[2]-orientA[2]==0): # if a and b are the same in y and z, then in plane direction must be accomplished by other method than adding to x component of origin
        orientB = (orientC[0],orientC[1]+1,orientC[2])
        print 'aligned with x'
    else:
        orientB = (orientC[0]+1,orientC[1],orientC[2]) #in plane to define y' and z' (taken in this case as projecting the origin in X)
    
    # Orientations will be used to specify a coordinate system using the rectangular method: 
    # https://help.3ds.com/2018/english/DSSIMULIA_Established/SIMACAEMODRefMap/simamod-c-orientation.htm?ContextScope=all&id=ec6276fa2757471495be493a34a37051#Pg0
    orientationPoints = [orientA,orientB,orientC]
    
    #Calculate centroid
    centroid1 = centroid(element, wp)
    
    # Save important data
    orientCenters[element.label-1] = centroid1
    orientList[element.label-1] = OrientationData(element.label,centroid1,orientationPoints)


for selement in sp_towSet.elements:
    # reset initial values
    minDist = 10000
    closestOrientationLabel = [0]

    # Get centroid for solid part
    centroidSolid = centroid(selement, sp)

    # For each wire element, test if this is the closest to the given solid element.  If it is, reassign closestOrientationLabel
    for welement in wp.elements:
        centroidWire = orientCenters[welement.label-1]

        d = distance(centroidSolid,centroidWire)  
        if d<minDist:
            minDist = d
            closestOrientationLabel = welement.label

    #Write closest element label to list of solid elements for each orientation
    # This list will be used to create an element set with like orientations
    orientList[closestOrientationLabel-1].solidElements.append(selement.label)
    
    
#Delete existing orientation features   
orientationNameString = 'scriptOrientation' 
for n in sp.features.keys():
    if orientationNameString in n:
        del sp.features[n]
for nord in range(0,len(sp.materialOrientations)):     
    del sp.materialOrientations[0]
    
# for each orientation: Create element set and assign orientation
for orien in orientList:        
    orienName = orientationNameString+str(orien.label)
    # Note orientations are stored in rectangular coordinate system format (a,b,c)
    sp.DatumCsysByThreePoints(name=orienName, coordSysType=CARTESIAN, origin=(
        orien.orient[2]), point1=(orien.orient[0]), point2=(orien.orient[1]))
        
    elementLabelList = orien.solidElements
    
    # If element label list is not empty (this shouldn't ever be but just in case)
    if elementLabelList != []:   
        #Create set from element labels
        sp.SetFromElementLabels(name=orienName,elementLabels=elementLabelList)
        region = sp.sets[orienName]
        #Get last entered datum using the last key in the list
        keyList = sp.datums.keys()
        orientation = sp.datums[keyList[-1]]
        sp.MaterialOrientation(region=region, 
            orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, fieldName='', 
            additionalRotationType=ROTATION_NONE, angle=0.0, 
            additionalRotationField='', stackDirection=STACK_3)