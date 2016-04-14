#coding:utf-8
'''
Created on 2016年3月14日 下午8:02:55

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: mirror pose 
'''
import os.path

import pymel.core as pm
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

import utils.mirror as mirror

def readControlsInfo(selection, info = '{0}/faceControls.info'.format(os.path.dirname(__file__))):
    namespace = selection.namespace()
    controlSet = []
    with open(info) as f:
        for line in f.readlines():
            try:
                control = pm.PyNode('{0}{1}'.format(namespace, line[:-2]))
            except:
                print '{0}{1} is not existed!'.format(namespace, line[:-2])
                control = None
            if control and not control.isLocked():
                controlSet.append(control)
                
    return controlSet       

def mirrorFacePose(controlSet):
    '''
    mirror the select character's facial pose
    '''
    currentTime = pm.currentTime()     
    poseDic = getPoseDic(controlSet)
    for k, v in poseDic.iteritems():
        mirrork = mirror.getMirror(k)
        if poseDic.has_key(mirrork):
            if pm.PyNode(k).shortName() == 'tx' or pm.PyNode(k).shortName() == 'rx':
                value = -1 * poseDic[mirrork]
            else :
                value = poseDic[mirrork]
            pm.PyNode(k).set(value)
            pm.PyNode(k).setKey()
            
                
def mirrorBodyPose(controlSet):
    '''
    mirror the select character's body pose
    '''
    currentTime = pm.currentTime()     
    poseDic = getPoseDic(controlSet)
    for k, v in poseDic.iteritems():
        mirrork = mirror.getMirror(k)
        if poseDic.has_key(mirrork):
            if pm.PyNode(k).shortName() == 'tx':
                value = -1 * poseDic[mirrork]
            elif mirrork == k and  pm.PyNode(k).shortName() == 'rz':
                value = -1 * poseDic[mirrork]
            else :
                value = poseDic[mirrork]
            pm.PyNode(k).set(value)
            pm.PyNode(k).setKey()
        
def getPoseDic(controlSet):
    poseDic = dict()
    for attr in controlSet:
        key = attr.name()
        value = attr.get()
        poseDic.setdefault(key, value)
    return poseDic

def runFace():
    sel = pm.ls(sl=1)
    controlSet = readControlsInfo(sel[0])
    mirrorFacePose(controlSet)

def runBody():
    sel = pm.ls(sl=1)
    controlSet = readControlsInfo(sel[0], info = '{0}/bodyControls.info'.format(os.path.dirname(__file__)))
    mirrorBodyPose(controlSet)
    
if __name__ == "__main__":
    runFace()
    runBody()