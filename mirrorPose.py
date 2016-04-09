#coding:utf-8
'''
Created on 2016年3月14日 下午8:02:55

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: mirror pose 
'''

import pymel.core as pm
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

import utils.mirror as mirror

def mirrorFacePose(character):
    '''
    mirror the select character's facial pose
    '''
    currentTime = pm.currentTime()     
    poseDic = getPoseDic(character)
    for k, v in poseDic.iteritems():
        mirrork = mirror.getMirror(k)
        if poseDic.has_key(mirrork):
            if pm.PyNode(k).shortName() == 'tx':
                value = -1 * poseDic[mirrork]
            else :
                value = poseDic[mirrork]
            pm.PyNode(k).set(value)
            pm.PyNode(k).setKey()
            
            
    
def mirrorBodyPose(character):
    '''
    mirror the select character's body pose
    '''
    pass

def getCharacterSet(selection):
    if selection:
        character = selection.inputs(type = 'objectSet')
        if character:
            return character[0]

        
def getPoseDic(character):
    poseDic = dict()
    for attr in character.members():
        key = attr.name()
        value = attr.get()
        poseDic.setdefault(key, value)
    return poseDic

def runFace():
    sel = pm.ls(sl=1)
    character = getCharacterSet(sel[0])
    mirrorFacePose(character)
    
if __name__ == "__main__":
    runFace