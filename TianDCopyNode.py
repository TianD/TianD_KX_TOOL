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
kSpaceDic = { 0: OpenMaya.MSpace.kObject, 1: OpenMaya.MSpace.kWorld }
kAxisDic = { 0: OpenMaya.MVector(1,0,0), 1: OpenMaya.MVector(0,1,0), 2: OpenMaya.MVector(0,0,1)}

class TianDCopyNode(OpenMayaMPx.MPxNode):

    templateGeom = OpenMaya.MObject()
    sourceGeom = OpenMaya.MObject()
    outputGeom = OpenMaya.MObject()
    spaceAttr = OpenMaya.MObject()
    upAxis = OpenMaya.MObject()
    sizeAttr = OpenMaya.MObject()
    
    def __init__(self):
        super(TianDCopyNode, self).__init__()
    
    def createMesh(self, sourceMesh, templateMesh, sizeShort, upaxisShort, spaceShort, newOutputData):
        
        # 根据输入的sourceMesh 和templateMesh, 创建新的Mesh
        # 新Mesh的形状是  将sourceMesh 复制到templateMesh 的每个点上形成的
        #
        mfnSourceMesh = OpenMaya.MFnMesh(sourceMesh)
        
        mfnTemplateMesh = OpenMaya.MFnMesh(templateMesh)
        
        numSourcePolygons = mfnSourceMesh.numPolygons()
        numSourceVertices = mfnSourceMesh.numVertices()
        
        # copyNum 就是 templateMesh的点的数量
        copyNum = mfnTemplateMesh.numVertices()
        
        # 新Mesh 包含的点的数量     
        newNumVertices = numSourceVertices*copyNum
        
        # 新Mesh 包含的poly面的数量
        newNumPolygons = numSourcePolygons*copyNum
         
        vertexArray = OpenMaya.MFloatPointArray() 
        mfnSourceMesh.getPoints(vertexArray)
        
        newVertexArray = OpenMaya.MPointArray()
        
        for i in xrange(newNumVertices):
            
            # 设置新Mesh 每个点的位置
            # 如sourceMesh 是个box, 有8个点. templateMesh 是个grid, 有4个点.
            # 那么新Mesh 就有8*4个点.
            # 其中每8个点组成一个box, 并便宜到 templateMesh 的点的位置上.
            #
            # i%numSourceVertices 用于计算新Mesh的点序号对应到 sourceMesh 的点序号. 如i=8, i%numSourceVertices=8%8=0, 就是新Mesh 的第8号点对应到 sourceMesh 的第0号点
            # int(i/numSourceVertices)%copyNum 用于计算新Mesh的点序号对应到 templateMesh 的点序号. 如 i=18, int(i/numSourceVertices)%copyNum=(18/8)%4=2%4=2, 就是新Mesh 的第18号点对应到 templateMesh 的第2号点.
            
            vertex = OpenMaya.MPoint()
            mfnSourceMesh.getPoint(i%numSourceVertices, vertex)
            
            templateVertex = OpenMaya.MPoint()
            mfnTemplateMesh.getPoint(int(i/numSourceVertices)%copyNum, templateVertex, kSpaceDic[spaceShort])
            
            # get templateMesh vertex's normal
            templateNormal = OpenMaya.MVector()
            mfnTemplateMesh.getVertexNormal(int(i/numSourceVertices)%copyNum, templateNormal, kSpaceDic[spaceShort])
            
            # make custom coordinate system
            up = kAxisDic[upaxisShort]
            customA = templateNormal
            customB = (customA ^ up).normal()
            customC = customA ^ customB
                
            # make size matrix
            sMatrixLst = [sizeShort, 0, 0, 0, 0, sizeShort, 0, 0, 0, 0, sizeShort, 0, 0, 0, 0, 1]
            sMatrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(sMatrixLst, sMatrix)
            
            # make rotate matrix
            if upaxisShort == 0:  
                rMatrixLst = [customA.x, customA.y, customA.z, 0, customB.x, customB.y, customB.z, 0, customC.x, customC.y, customC.z, 0, 0, 0, 0, 1]
            elif upaxisShort == 1:
                rMatrixLst = [customB.x, customB.y, customB.z, 0, customA.x, customA.y, customA.z, 0, customC.x, customC.y, customC.z, 0, 0, 0, 0, 1]
            elif upaxisShort == 2:
                rMatrixLst = [customB.x, customB.y, customB.z, 0, customC.x, customC.y, customC.z, 0, customA.x, customA.y, customA.z, 0, 0, 0, 0, 1]
            rMatrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(rMatrixLst, rMatrix)
            
            # make move matrix
            tMatrixLst = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, templateVertex.x, templateVertex.y, templateVertex.z, 1]
            tMatrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(tMatrixLst, tMatrix)
            
            # translate newMesh vertex 
            newVertex = vertex*sMatrix*rMatrix*tMatrix
            newVertexArray.append(newVertex)   
        
        newPolygonCounts = OpenMaya.MIntArray()
        
        # 根据SourceMesh 的poly的点的数量构造新Mesh 的poly点的数量
        for i in xrange(newNumPolygons):
            newPolygonCounts.append(mfnSourceMesh.polygonVertexCount(i%numSourcePolygons))
            
        newPolygonConnects = OpenMaya.MIntArray()
        
        # 根据SourceMesh 的点的链接结构链接新Mesh 的点
        for i in xrange(newNumPolygons):
            vertexList = OpenMaya.MIntArray()
            mfnSourceMesh.getPolygonVertices(i%numSourcePolygons, vertexList)
            newPolygonConnects += [vertexID + (i/numSourcePolygons)*numSourceVertices for vertexID in vertexList]
            
        mfnMesh = OpenMaya.MFnMesh()
        newMesh = mfnMesh.create(newNumVertices, newNumPolygons, newVertexArray, newPolygonCounts, newPolygonConnects, newOutputData)
        
        return newMesh
            
    def compute(self, plug, dataBlock):
        
        if plug == TianDCopyNode.outputGeom or plug == TianDCopyNode.spaceAttr :
            templateHandle = dataBlock.inputValue(TianDCopyNode.templateGeom)
            sourceHandle = dataBlock.inputValue(TianDCopyNode.sourceGeom)
            spaceHandle = dataBlock.inputValue(TianDCopyNode.spaceAttr)
            upaxisHandle = dataBlock.inputValue(TianDCopyNode.upAxis)
            sizeHandle = dataBlock.inputValue(TianDCopyNode.sizeAttr)
            outputHandle = dataBlock.outputValue(TianDCopyNode.outputGeom)
            
            templateMesh = templateHandle.asMesh()
            sourceMesh = sourceHandle.asMesh()
           
            dataCreator = OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            
            upaxisShort = upaxisHandle.asShort()
            spaceShort = spaceHandle.asShort()
            sizeShort = sizeHandle.asShort()
                        
            self.createMesh(sourceMesh, templateMesh, sizeShort, upaxisShort, spaceShort, newOutputData)  
            
            outputHandle.setMObject(newOutputData)
            dataBlock.setClean(plug)   
        
        else :
            return OpenMaya.kUnknownParameter
   
# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(TianDCopyNode())
         
# initializer
def nodeInitializer():
    
        # mesh attribute
        typedAttr = OpenMaya.MFnTypedAttribute()
        # input
        TianDCopyNode.templateGeom = typedAttr.create('templateMesh', 'template', OpenMaya.MFnData.kMesh)
        typedAttr.setStorable(1)
        typedAttr.setKeyable(0)
        typedAttr.setWritable(1)
        
        TianDCopyNode.sourceGeom = typedAttr.create('sourceMesh', 'source', OpenMaya.MFnData.kMesh)
        typedAttr.setStorable(1)
        typedAttr.setKeyable(0)
        typedAttr.setWritable(1)
        
        # output
        TianDCopyNode.outputGeom = typedAttr.create('outputMesh', 'out', OpenMaya.MFnData.kMesh)
        typedAttr.setStorable(1)
        typedAttr.setKeyable(0)
        typedAttr.setWritable(1)
        
        # enum attribute
        enumAttr = OpenMaya.MFnEnumAttribute()
        TianDCopyNode.spaceAttr = enumAttr.create('space', 'space', 1)
        enumAttr.addField('object', 0)
        enumAttr.addField('world', 1)
        enumAttr.setStorable(1)
        enumAttr.setKeyable(0)
        enumAttr.setWritable(1)
        
        TianDCopyNode.upAxis = enumAttr.create('upAxis', 'up', 0)
        enumAttr.addField('x', 0)
        enumAttr.addField('y', 1)
        enumAttr.addField('z', 2)
        enumAttr.setStorable(1)
        enumAttr.setKeyable(0)
        enumAttr.setWritable(1)
                
        # numeric attribute
        numAttr = OpenMaya.MFnNumericAttribute()
        TianDCopyNode.sizeAttr = numAttr.create('size', 's', OpenMaya.MFnNumericData.kShort, 1)
        enumAttr.setStorable(1)
        enumAttr.setKeyable(1)
        enumAttr.setWritable(1)
        
        try:
            TianDCopyNode.addAttribute( TianDCopyNode.templateGeom )
            TianDCopyNode.addAttribute( TianDCopyNode.sourceGeom )
            TianDCopyNode.addAttribute( TianDCopyNode.spaceAttr )
            TianDCopyNode.addAttribute( TianDCopyNode.upAxis )
            TianDCopyNode.addAttribute( TianDCopyNode.sizeAttr )
            TianDCopyNode.addAttribute( TianDCopyNode.outputGeom ) 
            TianDCopyNode.attributeAffects( TianDCopyNode.sourceGeom, TianDCopyNode.outputGeom )
            TianDCopyNode.attributeAffects( TianDCopyNode.templateGeom, TianDCopyNode.outputGeom )
            TianDCopyNode.attributeAffects( TianDCopyNode.spaceAttr, TianDCopyNode.outputGeom )
            TianDCopyNode.attributeAffects( TianDCopyNode.upAxis, TianDCopyNode.outputGeom )
            TianDCopyNode.attributeAffects( TianDCopyNode.sizeAttr, TianDCopyNode.outputGeom )
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