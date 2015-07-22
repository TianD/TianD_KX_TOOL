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
        
def duplicateSculptShape(base):
    if base.type() == "transform":
        pass
    elif base.type() == "mesh":
        base = base.getParent()
    else :
        return False
    sculptShape = pm.duplicate(base, name = "%s_blendshape" %base.name())[0]
    clearGeometry(sculptShape)
    return sculptShape

def clearGeometry(object):
    
    shapes = object.getShapes()
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
        print n
        finalMatrix +=bindPreMatrix[n]*transformationMatrix[n]*influenceWeight[n]
        print finalMatrix   
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
                setFinalPosition(sculptShape, i, finalPosition)

if __name__ == "__main__":
    base = getBaseShape()
    sculpt = duplicateSculptShape(base)
    clearGeometry(sculpt)
    baseShape = base.getShape()
    sculptShape = sculpt.getShape()
    
    doCorrection(baseShape, sculptShape)
    
    