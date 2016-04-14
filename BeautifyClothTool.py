#coding:utf-8
'''
Created on 2016年2月19日 下午5:37:28

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: Beautify cloth tool
'''
import re

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import uiTool
import pymel.core as pm
import utils.convert as convert
import utils.follicle as follicle

uiPath = uiTool.getUIPath("TianD_KX_TOOL\\BCT.ui")
form_class, base_class = uic.loadUiType(uiPath)
class BeautifyClothToolWin(form_class, base_class):
    
    def __init__(self, parent = uiTool.getMayaWindow()):
                
        super(BeautifyClothToolWin, self).__init__(parent) 
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.createBtn.clicked.connect(self.createCmd)
        self.paintBtn.clicked.connect(self.paintCmd)
        self.bakeBtn.clicked.connect(self.bakeCmd)
        self.deleteBtn.clicked.connect(self.deleteCmd)
        self.allBtn.clicked.connect(self.allCmd)
        
    def createCmd(self):
        sel = pm.ls(sl=1, fl=1)
        selVertex = convert.toVertex(sel)
        BCCs = getBCC()
        if BCCs:
            maxNum = int(BCCs[-1].name().split('BCT_ctrl')[-1].split('_MASTER')[0])
        else :
            maxNum = 0
        cluster = createCluster(selVertex, "BCT_ctrl{0}".format(maxNum+1))
        fol = createFol(selVertex, "BCT_ctrl{0}".format(maxNum+1))
        ctrl = createCtrl(fol, cluster[1], "BCT_ctrl{0}".format(maxNum+1))
        pm.select(ctrl)
        
    def paintCmd(self):
        sel = pm.ls(sl=1)
        m = re.match("BCT_ctrl\d*_Ctrl", sel[0].name())
        if m:
            cluster = sel[0].replace("Ctrl","Clu")
            pm.select(getGeometry(pm.PyNode(cluster)))
            pm.mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "cluster.{0}.weights" );'.format(cluster))
        else :
            print "selection is not BCT!!!"
            
    def bakeCmd(self):
        sel = pm.ls(sl=1)
        min = pm.playbackOptions(q=1, min=1)
        max = pm.playbackOptions(q=1, max=1)
        m = re.match("BCT_ctrl\d*_Ctrl", sel[0].name())
        if m:
            pm.bakeResults(sel[0], t =(min, max), simulation=True)
        else :
            print "selection is not BCT!!!"
    
    def deleteCmd(self):
        sel = pm.ls(sl=1)
        BCMs = [i.name().replace("Ctrl", "MASTER") for i in sel if re.match("BCT_ctrl\d*_Ctrl", i.name())]
        pm.delete(BCMs)
    
    def allCmd(self):
        BCMs = getBCC()
        BCCs = [i.name().replace("MASTER", "Ctrl") for i in BCMs]
        pm.select(BCCs)
        
def getBCC():
    BCCs = pm.ls(regex = "BCT_ctrl\d*_MASTER", type = "transform")
    return BCCs

def getGeometry(cluster):
    geo = cluster.getGeometry()
    return geo

def createCluster(vertexs, name):
    mesh = vertexs[0].node()
    cluster = pm.cluster(mesh, name = "{0}_Clu".format(name))
    pm.percent(cluster[0], mesh.vtx, v=0)
    pm.percent(cluster[0], vertexs, v=1)
    cluster[-1].visibility.set(0)
    return cluster
    
def createFol(selection, name):
    vertexs = convert.toVertex(selection)
    mesh = vertexs[0].node()
    posLst = [v.getPosition(space = "world") for v in vertexs]
    pos = sum(posLst)/len(posLst)
    fol = follicle.create_follicle_by_position(mesh.getParent().name(), pos)
    fol = pm.rename(fol, "{0}_fol".format(name))
    folShape = fol.getShape()
    fol.r.unlock()
    fol.r.disconnect()
    fol.r.set(0,0,0)
    folShape.visibility.set(0)
    return pm.PyNode(fol)

def createCtrl(fol, clusterHandle, name):
    masterGrp = pm.group(em=1, name = "{0}_MASTER".format(name))
    locCtrl = pm.group(em=1, name = "{0}_LOC".format(name))
    upCtrl = pm.group(em=1, name = "{0}_UP".format(name))
    ctrl = pm.group(em=1, name = "{0}_Ctrl".format(name))
    ctrl.setParent(upCtrl)
    upCtrl.setParent(locCtrl)
    locCtrl.setParent(fol)
    locCtrl.t.set(0,0,0)
    
    md = pm.createNode("multiplyDivide", name = "{0}_MD".format(name))
    clusterHandle.t >> md.input1
    md.input2.set(-1,-1,-1)
    md.output >> upCtrl.t
    
    ctrl.t >> clusterHandle.t
    ctrl.r >> clusterHandle.r
    
    ctrl.displayHandle.set(1)
    fol.setParent(masterGrp)
    clusterHandle.setParent(masterGrp)
    
    currentTime = pm.currentTime(q=1)
    ctrl.t.setKey(t = currentTime)
    ctrl.t.setKey(t = currentTime + 5)
    ctrl.t.setKey(t = currentTime - 5)
    ctrl.r.setKey(t = currentTime)
    ctrl.r.setKey(t = currentTime + 5)
    ctrl.r.setKey(t = currentTime - 5)
    
    return ctrl    
    
def run():
    win = BeautifyClothToolWin()
    win.show()

if __name__ == "__main__":
    run()