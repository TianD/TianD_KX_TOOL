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

###
# create original mesh
numVertices = 5
numPolygons = 2

vertexLst = [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[-2,-2,0]]

vertexArray = OpenMaya.MFloatPointArray()

for vertex in vertexLst:
    omVertex = OpenMaya.MFloatPoint(vertex[0], vertex[1], vertex[2])
    vertexArray.append(omVertex)

mfnMesh = OpenMaya.MFnMesh()

counts = [4,3]
polygonCounts = OpenMaya.MIntArray()

for i in counts:
    polygonCounts.append(i)
    
connects = [0,1,2,3,4,3,2]
polygonConnects = OpenMaya.MIntArray()

for i in connects:
    polygonConnects.append(int(i))
    
mfnMesh.create(numVertices, numPolygons, vertexArray, polygonCounts, polygonConnects)
###


###
# copy polygons
sel = pymel.core.ls(sl=1)[0]
originalMesh = sel.__apiobject__()

mfnMesh = OpenMaya.MFnMesh(originalMesh)

numPolygons = mfnMesh.numPolygons()
numVertices = mfnMesh.numVertices()

mergeVertices = True
pointTolerance = 0.001

vertexArrayCopy = OpenMaya.MPointArray()

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
