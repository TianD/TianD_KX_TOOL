#coding:utf-8
'''
Created on 2016年5月4日 上午11:32:15

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:

'''
import re

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import pymel.core as pm

import uiTool
import utils.objSet as objSet

uiPath = uiTool.getUIPath("TianD_KX_TOOL\\SmoothSetWin.ui")
form_class, base_class = uic.loadUiType(uiPath)
class SmoothSetToolWin(form_class, base_class):
    
    def __init__(self, parent = uiTool.getMayaWindow()):
                
        super(SmoothSetToolWin, self).__init__(parent) 
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.smoothPushButton.clicked.connect(self.smoothCmd)
    
    def smoothCmd(self):
        smoothDic = dict()
        smoothKey = '{0}'.format(self.smoothComboBox.currentText()).upper()
        objLst = pm.ls(sl=1)
        smoothDic.setdefault(smoothKey,objLst)
        createSmoothSet(**smoothDic)     

def createSmoothSet(**kwargs):
    partition = objSet.createPartition('SMOOTH_PARTITION', [], increment = False)
    if kwargs.has_key('SMOOTH_0'):
        set0 = objSet.createObjectSet('SMOOTH_0', kwargs['SMOOTH_0'], exclusiveness = True, partition = partition, increment = False)
    else :
        set0 = objSet.createObjectSet('SMOOTH_0', [], exclusiveness = True, partition = partition, increment = False)
    if kwargs.has_key('SMOOTH_1'):
        set1 = objSet.createObjectSet('SMOOTH_1', kwargs['SMOOTH_1'], exclusiveness = True, partition = partition, increment = False)
    else :
        set1 = objSet.createObjectSet('SMOOTH_1', [], exclusiveness = True, partition = partition, increment = False)
    if kwargs.has_key('SMOOTH_2'):
        set2 = objSet.createObjectSet('SMOOTH_2', kwargs['SMOOTH_2'], exclusiveness = True, partition = partition, increment = False)
    else :
        set2 = objSet.createObjectSet('SMOOTH_2', [], exclusiveness = True, partition = partition, increment = False)
    smoothSet = objSet.createObjectSet('SMOOTH_SET', [set0,set1,set2], exclusiveness = False, partition = None, increment = False)
        
    return smoothSet
        
def setDisplaySmoothLevel(obj, level):
    obj.smoothLevel.set(level)
    return obj

def run():
    win = SmoothSetToolWin()
    win.show()

if __name__ == "__main__":
    run()