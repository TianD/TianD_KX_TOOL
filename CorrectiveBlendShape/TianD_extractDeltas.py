#coding:utf-8
'''
Created on 2015年7月24日

@author: TianD
'''
import pymel.core as pm

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

def extractDeltasDuplicateMesh():
    #duplicate skinned original geometry
    
    #select skinned geometry
    sel = pm.ls(sl=1)
    if len(sel) == 1:
        sel = sel[0]
        shape = sel.getShape()
    else :
        return False
    
    #set all deformers's envelope to 0
    closeDeformer(shape)
    
    #duplicate skinned geometry
    dup = pm.duplicate(sel, name = "%s_dup" %sel.name())[0]
    clearGeometry(dup)
    
    #set all deformers's envelope to 1
    openDeformer(shape)
    
    return dup

def performExtractDeltas():
    