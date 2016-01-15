#coding:utf-8
'''
Created on 2015年9月7日 下午2:18:25

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import sys
import pymel.core
import maya.OpenMaya as OpenMaya 
import maya.OpenMayaMPx as OpenMayaMPx

# consts
kCopyNodeName = "TianDCopyNode"
kCopyNodeId = OpenMaya.MTypeId(0x99000)

class TianDCopyNode(OpenMayaMPx.MPxNode):

    templateGeom = OpenMaya.MObject()
    sourceGeom = OpenMaya.MObject()
    outputGeom = OpenMaya.MObject()
    
    def __init__(self):
        super(TianDCopyNode, self).__init__()
        
    
    def createMesh(self, sourceMesh, templateMesh, newOutputData):
        
        mfnSourceMesh = OpenMaya.MFnMesh(sourceMesh)
        
        mfnTemplateMesh = OpenMaya.MFnMesh(templateMesh)
        
        numSourcePolygons = mfnSourceMesh.numPolygons()
        numSourceVertices = mfnSourceMesh.numVertices()
        
        copyNum = mfnTemplateMesh.numVertices()
             
        newNumVertices = numSourceVertices*copyNum
        
        newNumPolygons = numSourcePolygons*copyNum
        
        vertexArray = OpenMaya.MFloatPointArray()
         
        mfnSourceMesh.getPoints(vertexArray)
        
        newVertexArray = OpenMaya.MFloatPointArray()
        
        for i in xrange(newNumVertices):
            vertex = OpenMaya.MPoint()
            mfnSourceMesh.getPoint(i%numSourceVertices, vertex)
            vector = OpenMaya.MFloatVector(0,0,int(i/numSourceVertices)*offsetZ)
            newVertex = OpenMaya.MFloatPoint(vertex.x + vector.x, vertex.y + vector.y, vertex.z + vector.z)
            newVertexArray.append(newVertex)
        
        newPolygonCounts = OpenMaya.MIntArray()
        
        
        for i in xrange(newNumPolygons):
            newPolygonCounts.append(mfnMesh.polygonVertexCount(i%numSourcePolygons))
            
        newPolygonConnects = OpenMaya.MIntArray()
        
        for i in xrange(newNumPolygons):
            vertexList = OpenMaya.MIntArray()
            mfnSourceMesh.getPolygonVertices(i%numSourcePolygons, vertexList)
            newPolygonConnects += [vertexID + (i/numSourcePolygons)*numSourceVertices for vertexID in vertexList]
            
        mfnMesh = OpenMaya.MFnMesh()
        newMesh = mfnMesh.create(newNumVertices, newNumPolygons, newVertexArray, newPolygonCounts, newPolygonConnects, newOutputData)
        
        return newMesh
        
    
    def compute(self, plug, dataBlock):
        
        if plug == TianDCopyNode.outputGeom:
            templateHandle = dataBlock.inputValue(TianDCopyNode.templateGeom)
            sourceHandle = dataBlock.inputValue(TianDCopyNode.sourceGeom)
            outputHandle = dataBlock.outputValue(TianDCopyNode.outputGeom)
            
            templateMesh = templateHandle.asMesh()
            sourceMesh = sourceHandle.asMesh()
           
            dataCreator = OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            
            self.createMesh(sourceMesh, templateMesh, newOutputData)
            
            outputHandle.setMObject(newOutputData)
            data.setClean(plug)
        
        else :
            return OpenMaya.kUnknownParameter

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(TianDCopyNode())
         
# initializer
def nodeInitializer():
        # template mesh
        typedAttr = OpenMaya.MFnTypedAttribute()
        TianDCopyNode.templateGeom = typedAttr.create('templateMesh', 'template', OpenMaya.MFnData.kMesh)
        TianDCopyNode.sourceGeom = typedAttr.create('sourceMesh', 'source', OpenMaya.MFnData.kMesh)
        TianDCopyNode.outputGeom = typedAttr.create('outputMesh', 'out', OpenMaya.MFnData.kMesh)
        
        try:
                TianDCopyNode.addAttribute( TianDCopyNode.templateGeom )
                TianDCopyNode.addAttribute( TianDCopyNode.sourceGeom )
                TianDCopyNode.addAttribute( TianDCopyNode.outputGeom )
                TianDCopyNode.attributeAffects( TianDCopyNode.sourceGeom, TianDCopyNode.outputGeom )
                TianDCopyNode.attributeAffects( TianDCopyNode.templateGeom, TianDCopyNode.outputGeom )
        except:
                sys.stderr.write( "Failed to create attributes of %s node\n" % kCopyNodeName )
        
# initialize the script plug-in
def initializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.registerNode( kCopyNodeName, kCopyNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDeformerNode )
        except:
                sys.stderr.write( "Failed to register node: %s\n" % kCopyNodeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterNode( kCopyNodeId )
        except:
                sys.stderr.write( "Failed to unregister node: %s\n" % kCopyNodeName )

                
###
# create original mesh
# numVertices = 5
# numPolygons = 2
# 
# vertexLst = [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[-2,-2,0]]
# 
# vertexArray = OpenMaya.MFloatPointArray()
# 
# for vertex in vertexLst:


#     omVertex = OpenMaya.MFloatPoint(vertex[0], vertex[1], vertex[2])
#     vertexArray.append(omVertex)
# 
# mfnMesh = OpenMaya.MFnMesh()
# 
# counts = [4,3]
# polygonCounts = OpenMaya.MIntArray()
# 
# for i in counts:
#     polygonCounts.append(i)
#     
# connects = [0,1,2,3,4,3,2]
# polygonConnects = OpenMaya.MIntArray()
# 
# for i in connects:
#     polygonConnects.append(int(i))
#     
# mfnMesh.create(numVertices, numPolygons, vertexArray, polygonCounts, polygonConnects)
###


###
# copy polygons
sel = pymel.core.ls(sl=1)[0]
originalMesh = sel.__apiobject__()

mfnMesh = OpenMaya.MFnMesh(originalMesh)

numPolygons = mfnMesh.numPolygons()
numVertices = mfnMesh.numVertices()

copyNum = 5

offsetZ = 1    


newNumVertices = numVertices*copyNum

newNumPolygons = numPolygons*copyNum

vertexArray = OpenMaya.MFloatPointArray()
 
mfnMesh.getPoints(vertexArray)

newVertexArray = OpenMaya.MFloatPointArray()

for i in xrange(newNumVertices):
    vertex = OpenMaya.MPoint()
    mfnMesh.getPoint(i%numVertices, vertex)
    vector = OpenMaya.MFloatVector(0,0,int(i/numVertices)*offsetZ)
    newVertex = OpenMaya.MFloatPoint(vertex.x + vector.x, vertex.y + vector.y, vertex.z + vector.z)
    newVertexArray.append(newVertex)

newPolygonCounts = OpenMaya.MIntArray()


for i in xrange(newNumPolygons):
    newPolygonCounts.append(mfnMesh.polygonVertexCount(i%numPolygons))
    
print newPolygonCounts
newPolygonConnects = OpenMaya.MIntArray()

for i in xrange(newNumPolygons):
    vertexList = OpenMaya.MIntArray()
    mfnMesh.getPolygonVertices(i%numPolygons, vertexList)
    newPolygonConnects += [vertexID + (i/numPolygons)*numVertices for vertexID in vertexList]
    
print newPolygonConnects
mfnMesh.create(newNumVertices, newNumPolygons, newVertexArray, newPolygonCounts, newPolygonConnects)

# for i in xrange(copyNum):
#     polyNum = mfnMesh.numPolygons()
#     for j in xrange(polyNum):
#         polyvertices = OpenMaya.MIntArray()
#         mfnMesh.getPolygonVertices(j, polyvertices)
#         for h in polyvertices:
#             pos = OpenMaya.MPoint()
#             mfnMesh.getPoint(h, pos)
#             copypos = pos + OpenMaya.MVector(0,0,offsetZ)
#             vertexArrayCopy.append(copypos)
#         mfnMesh.addPolygon(vertexArrayCopy, mergeVertices, pointTolerance)
#         vertexArrayCopy.clear()


# faceList = OpenMaya.MIntArray()  
# for i in xrange(numPolygons):
#     faceList.append(i)
# for i in xrange(copyNum):
#     translation = OpenMaya.MFloatVector(0,0, offsetZ*(i+1))
#     mfnMesh.duplicateFaces(faceList,translation)
###
