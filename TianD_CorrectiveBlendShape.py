#coding:utf-8
'''
Created on 2015/7/22

@author: TianD

description: corrective blendshape

reference: https://circecharacterworks.wordpress.com/2011/03/26/presentation/
'''

import pymel.core as pm

def getBaseShape():
    sel = pm.ls(sl=1)
    
    if len(sel) == 1:
        if sel[0].getChildren():
            basemesh = sel[0].getShape()
            if basemesh and basemesh.type() == "mesh":
                return sel[0]
    else :
        return False
        
def duplicateSculptShape(obj):
    if obj.type() == "transform":
        transform = obj
    elif obj.type() == "mesh":
        transform = obj.getParent()
    else :
        return False
    closeDeformer(transform)
    sculptShape = pm.duplicate(transform, name = "%s_blendshape" %transform.name())[0]
    clearGeometry(sculptShape)
    openDeformer(transform)
    pm.blendShape(transform, sculptShape, origin = "local", w=(0,1))
    tweak = sculptShape.getShape().inputs(type = "tweak")[0]
    pm.delete(tweak)
    return sculptShape

def closeDeformer(obj):
    if obj.type() == "transform":
        shape = obj.getShape()
    elif obj.type() == "mesh":
        shape = obj
    else :
        return False
    deformers =[h for h in shape.listHistory() if h.hasAttr("envelope")]
    for d in deformers:
        d.envelope.set(0)
    return True
    
def openDeformer(obj):
    if obj.type() == "transform":
        shape = obj.getShape()
    elif obj.type() == "mesh":
        shape = obj
    else :
        return False
    deformers =[h for h in shape.listHistory() if h.hasAttr("envelope")]
    for d in deformers:
        if not d.envelope.get():
            d.envelope.set(1)
    return True
    
def clearGeometry(obj):
    
    shapes = obj.getShapes()
    if shapes:
        for shape in shapes:
            if shape.isIntermediate() :
                pm.delete(shape)
    else :
        return False
    return True

def getSkinCluster(baseShape):
    if baseShape.type() == "mesh":
        skinName = pm.mel.eval( 'findRelatedSkinCluster("%s")'%baseShape.name() )
        if skinName:
            return pm.PyNode(skinName)
        else :
            return False
    else :
        return False
    
def getInfluenceWeight(baseShape, skinNode):
        influenceWeight = list(skinNode.getWeights(baseShape))
        return influenceWeight
    
def getWeightedInverseMatrix(numInfluence, bindPreMatrix, transformationMatrix, influenceWeight):
    finalMatrix = pm.dt.Matrix([0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0])
    for n in range(numInfluence):
        if transformationMatrix[n] :
            finalMatrix +=bindPreMatrix[n]*transformationMatrix[n]*influenceWeight[n]  
        else :
            pass
    inverseMatrix = finalMatrix.inverse()
    return inverseMatrix

def getFinalPosition(sculptShape, vtxID, inverseMatrix):
    if sculptShape.type() == "mesh":
        try:
            pos = sculptShape.vtx[vtxID].getPosition()
        except:
            return False
        finalPosition = pos*inverseMatrix
        return finalPosition

def setFinalPosition(sculptShape, vtxID, vertexPosition):
    if sculptShape.type() == "mesh":
        try:
            sculptShape.vtx[vtxID].setPosition(vertexPosition)
            return True
        except:
            return False
    else :
        return False
        
def doCorrection(baseShape, sculptShape):
    
    skinNode = getSkinCluster(baseShape)
    numInfluence = skinNode.numInfluenceObjects()
    bindPreMatrix = skinNode.bindPreMatrix.get()
    transformationMatrix = skinNode.matrix.get()
    finalPositionStorage = []
    for i,v in enumerate(baseShape.vtx):
        base_pos = v.getPosition()
        sculpt_pos = sculptShape.vtx[i].getPosition()
        diff = sculpt_pos - base_pos
        
        if diff.x >= -0.001 and diff.x <= 0.001 and diff.y >= -0.001 and diff.y <= 0.001 and diff.z >= -0.001 and diff.z <= 0.001:
            pass
        else :
            weight = getInfluenceWeight(v, skinNode)[0]
            if weight <= 0.0001 :
                pass
            else :
                inverseMatrix = getWeightedInverseMatrix(numInfluence, bindPreMatrix, transformationMatrix, weight)
                finalPosition = getFinalPosition(sculptShape, i, inverseMatrix)
                finalPositionStorage.append(finalPosition)
                setFinalPosition(sculptShape, i, finalPosition)
                #dis = finalPosition - base_pos
                #sculptShape.vtx[i].translateBy(dis)

if __name__ == "__main__":
    base = getBaseShape()
    sculpt = duplicateSculptShape(base)
    baseShape = base.getShape()
    sculptShape = sculpt.getShape()
    
    doCorrection(baseShape, sculptShape)