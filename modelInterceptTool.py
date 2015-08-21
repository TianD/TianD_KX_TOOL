#coding:utf-8
'''
Created on 2015年8月21日 下午5:02:44

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
#coding:utf-8
'''
Created on 2015/7/8

@author: TianD
'''

import sys

path = "E:\\Scripts\\Eclipse\\TianD_KX_TOOL"
path in sys.path or sys.path.insert(0,path)

import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import pymel.core as pm
import uiTool
import kxTool
reload(kxTool)
reload(uiTool)

uiPath = os.environ['XBMLANGPATH'].split(";")[1] + "/TianD_KX_TOOL"
form_class, base_class = uic.loadUiType('%s/modelInterceptWindow_all.ui' %uiPath)
class MODELInterceptTool(form_class, base_class):
    
    def __init__(self, parent = uiTool.getMayaWindow()):
                
        super(MODELInterceptTool, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMaximumHeight(376)
        self.setMaximumWidth(203)
        
        self.setWindowIcon(QtGui.QIcon("%s/bullet_deny.png" %uiPath))
        
        for btn in self.findChildren(QtGui.QPushButton, QtCore.QRegExp("check\d+Btn")):
            btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
            btn.setStyleSheet('border-image:url(%s/question.png);' %uiPath)
        
        
        self.check0Btn.clicked.connect(self.checkSceneName)               #物体历史
        self.check1Btn.clicked.connect(self.getAnimCamera)                #位移变换
        
        self.checkAllBtn.clicked.connect(self.checkAll)
        self.skipAllBtn.clicked.connect(self.skipAll)
        
        self.flag0 = None
        self.flag1 = None

        
        self.checkAll()
                    
    def checkSceneName(self):
        flag = self.anim.checkSceneName()
        if flag :
            self.check0Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
            self.check0Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
            self.flag0 = True
        else :
            self.check0Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check0Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag0 = False
        if self.flag0 is True:
            pass
        else :
            pass
    
    def camScale1(self):
        if self.flag1 is None:
            pass
        elif self.flag3 is None and self.flag1 is True:
            flag = self.anim.camScale1()
            if flag :
                self.check3Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
                self.check3Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
                self.flag3 = True
            else :
                self.check3Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
                self.check3Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
                self.flag3 = False
        elif self.flag3 is True:
            pass
        elif self.flag1 is False:
            self.check3Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check3Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag3 = False
        elif self.flag3 is False and self.flag1 is True:
            pm.select(self.anim.camera)
        else :
            pass
            
    def checkAll(self):
        self.anim.getSceneName()
        self.anim.analyzeSceneName()
        if not self.skip9.checkState() :
            self.flag9 = None
            self.checkExt()
        if not self.skip0.checkState():
            self.flag0 = None
            self.checkSceneName()
        if not self.skip1.checkState() :
            self.flag1 = None
            self.getAnimCamera()        
            
        if (self.flag1 or self.skip1.checkState()) and \
            (self.flag2 or self.skip2.checkState()):
            self.close()
            return True
        else :
            return False
    
    def skipAll(self):
        self.close()
        return True
        
class MODELIntercept(kxTool.KXTool):
    
    def __init__(self):
        '''
                 模型规范拦截:
            1.模型历史;[OK]
            2.位移清零;[OK]
        '''
        super(MODELIntercept, self).__init__()
        self.getSceneName()
        self.analyzeSceneName()
        self.topGroups = ["persp", "top", "front", "side", "char", "set", "prop"]
        
    def checkSceneName(self):
        try:
            frameRange = pm.mel.eval('idmtProject -timeLine "%s.mb"' %self.sceneName)
            if frameRange :
                return True
            else :
                return False
        except:
            pass
    
    def getAnimCamera(self):
        if self.sceneName:
            cameraName = "cam_%s_%s_%s" %(self.episodeNumber, self.sessionNumber, self.sceneNumber)
            try:
                self.camera = pm.PyNode(cameraName)
                self.topGroups.append(self.camera.getParent(-1))
                return True
            except:
                return False
    
def show():
    if uiTool.windowExisted("modelInterceptWindow"):
        pass
    else :
        a = MODELInterceptTool()
        a.show()
      
show()  
if __name__ == "__main__":
    show()