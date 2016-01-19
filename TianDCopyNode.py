#coding:utf-8
'''
Created on 2016年1月16日  22:18:25

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

#
# how to use
#
# import pymel.core as pm
# source = pm.polyCube(ch=0)[0].getShape()
# template = pm.polyPlane(ch=0)[0].getShape()
# copy = pm.createNode("TianDCopyNode")
# source.outMesh >> copy.source
# template.outMesh >> copy.template
# show = pm.createNode("transform", name = "show1")
# showShape = pm.createNode("mesh", name = "showShape1", parent = show)
# copy.out >> showShape.inMesh
#


import sys
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
        #sys.stdout.write("numSourcePolygons: %s, numSourceVertices: %s" %(numSourcePolygons, numSourceVertices))
        
        copyNum = mfnTemplateMesh.numVertices()
             
        newNumVertices = numSourceVertices*copyNum
        
        newNumPolygons = numSourcePolygons*copyNum
        
        vertexArray = OpenMaya.MFloatPointArray()
         
        mfnSourceMesh.getPoints(vertexArray)
        
        newVertexArray = OpenMaya.MFloatPointArray()
                
        #offsetZ = 0
        for i in xrange(newNumVertices):
            vertex = OpenMaya.MPoint()
            mfnSourceMesh.getPoint(i%numSourceVertices, vertex)
            #vector = OpenMaya.MFloatVector(0,0,int(i/numSourceVertices)*offsetZ)
            templateVertex = OpenMaya.MPoint()
            mfnTemplateMesh.getPoint(int(i/numSourceVertices)%copyNum, templateVertex)
            vector = OpenMaya.MFloatVector(templateVertex.x, templateVertex.y, templateVertex.z)
            newVertex = OpenMaya.MFloatPoint(vertex.x + vector.x, vertex.y + vector.y, vertex.z + vector.z) 
            #sys.stdout.write("num: %s, %s, %s, %s\n" %(i, newVertex.x, newVertex.y, newVertex.z))
            newVertexArray.append(newVertex)
        
        newPolygonCounts = OpenMaya.MIntArray()
        
        
        for i in xrange(newNumPolygons):
            newPolygonCounts.append(mfnSourceMesh.polygonVertexCount(i%numSourcePolygons))
            
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
            dataBlock.setClean(plug)
        
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