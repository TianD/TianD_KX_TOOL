#coding:utf-8
'''
Created on 2015/7/8

@author: TianD
'''
import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import pymel.core as pm
import uiTool
import kxMayaTool
reload(kxMayaTool)
reload(uiTool)

uiPath = os.environ['XBMLANGPATH'].split(";")[1] + "/TianD_KX_TOOL"
form_class, base_class = uic.loadUiType('%s/animInterceptWindow.ui' %uiPath)
class ANIMInterceptTool(form_class, base_class):
    
    def __init__(self, parent = uiTool.getMayaWindow()):
                
        super(ANIMInterceptTool, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("%s/bullet_deny.png" %uiPath))
        self.check1Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check2Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check3Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check4Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check5Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check6Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check7Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        self.check8Btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
        
        
        self.anim = ANIMIntercept()
        
        self.check1Btn.clicked.connect(self.getAnimCamera)
        self.check2Btn.clicked.connect(self.camLock)
        self.check3Btn.clicked.connect(self.camScale1)
        self.check4Btn.clicked.connect(self.getNeedlessCamera)
        self.check5Btn.clicked.connect(self.framesIntercept)
        #self.check6Btn.clicked.connect(self.anim.getAnimCamera())        #删除norender以外的层
        #self.check7Btn.clicked.connect(self.anim.getAnimCamera())        #整理大纲
        #self.check8Btn.clicked.connect(self.anim.)                       #删除空组
        
        #self.checkAllBtn.clicked.connect(self.checkAll)
        #self.skipAllBtn.clicked.connect(self.skipAll)
        
        self.flag1 = None
        self.flag2 = None
        self.flag3 = None
        self.flag4 = None
        self.flag5 = None
        self.flag6 = None
        self.flag7 = None
        self.flag8 = None
        
        self.allFlag = self.checkAll()
    
    def getAnimCamera(self):
        flag = self.anim.getAnimCamera()
        if flag :
            self.check1Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
            self.check1Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
            self.flag1 = True
        else :
            self.check1Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check1Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag1 = False
        if self.flag1 is True:
            pm.select(self.anim.camera)
        else :
            pass
    
    def camLock(self):
        if self.flag1 is None:
            pass
        elif self.flag2 is None and self.flag1 is True :
            flag = self.anim.camLock()
            if flag :
                self.check2Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
                self.check2Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
                self.flag2 = True
            else :
                self.check2Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
                self.check2Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
                self.flag2 = False
        elif self.flag2 is True:
            pass
        elif self.flag1 is False:
            self.check2Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check2Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag2 = False
        elif self.flag2 is False and self.flag1 is True:
            pm.select(self.anim.camera)
        else :pass
    
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
            
    def getNeedlessCamera(self):
        if self.flag1 is None:
            pass
        elif self.flag4 is None and self.flag1 is True:
            flag = self.anim.getNeedlessCamera()
            if flag :
                self.check4Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
                self.check4Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
                self.flag4 = True
            else :
                self.check4Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
                self.check4Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
                self.flag4 = False
        elif self.flag4 is True:
            pass
        elif self.flag1 is False:
            self.check4Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check4Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag4 = False
        elif self.flag4 is False and self.flag1 is True:
            pm.select(self.anim.needlessCamera)
        else :
            pass
        
    def framesIntercept(self):
        if self.flag5 is None:
            flag = self.anim.framesIntercept()
            if flag :
                self.check5Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
                self.check5Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
                self.flag5 = True
            else :
                self.check5Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
                self.check5Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
                self.flag5 = False
        elif self.flag5 is True:
            pass
        else:
            pass
                                           
    def checkAll(self):
        self.getAnimCamera()
        self.camLock()
        self.camScale1()
        self.getNeedlessCamera()
        self.framesIntercept()
        if self.flag1 and self.flag2 and self.flag3 and self.flag4 and self.flag5:
            return True
        else :
            return False
    
    def skipAll(self):
        return True
        
class ANIMIntercept(kxMayaTool.KXTool):
    
    def __init__(self):
        '''
        13 动画规范拦截:
            1.相机锁定;[OK]
            2.相机缩放归1;[OK]
            3.清理除norender以外的层;
            4.清理空组;
            5.拦截cam的命名和文件命名不一样;(重要的)[OK]
            6.拦截帧数和数据库不一样;(重要的)[OK]
            7.清理多余的摄像机;[OK]
            8.自动在outerline里吧角色归到char组,场景归到set组,道具归到prop组;
        '''
        super(ANIMIntercept, self).__init__()
        self.analyzeSceneName()
        
    def getAnimCamera(self):
        #self.analyzeSceneName()
        if self.sceneName:
            cameraName = "cam_%s_%s_%s" %(self.episodeNumber, self.sessionNumber, self.sceneNumber)
            try:
                self.camera = pm.PyNode(cameraName)
                return True
            except:
                return False
    
    def getFrameRange(self):
        self.min = pm.playbackOptions(q = 1, min = 1)
        self.max = pm.playbackOptions(q = 1, max = 1)
        self.start = pm.playbackOptions(q = 1, animationStartTime = 1)
        self.end = pm.playbackOptions(q = 1, animationEndTime = 1)
        if self.start != self.min:
            pm.playbackOptions(e = 1, animationStartTime = self.min)
        if self.end != self.max:
            pm.playbackOptions(e = 1, animationEndTime = self.max)
        
    def getNeedlessCamera(self):
        cameraLst = [cam.getParent() for cam in pm.ls(type = 'camera')]
        self.needlessCamera = [cam for cam in cameraLst if cam not in self.defaultCameraNameLst and cam != self.camera]
        if self.needlessCamera :
            return False
        else :
            return True
    
    def camScale1(self):
        scale = self.camera.s.get()
        if scale != pm.dt.Vector([1.0, 1.0, 1.0]):
            return False
        else:
            return True
    
    def camLock(self):
        cbAttr = self.camera.listAttr(k=1) + self.camera.getShape().listAttr(k=1)
        for attr in cbAttr:
            if not attr.isLocked():
                return False
            else :
                pass
        return True
            
    def framesIntercept(self):
#         self.getExcel()
#         sheet = excelTool.openExcel(self.path[0])
#         rowID = excelTool.locate(sheet, self.sessionNumber, self.sceneNumber)
#         frameRange = excelTool.getFrameRange(sheet, rowID[0])
        frameRange = pm.mel.eval('idmtProject -timeLine "%s.mb"' %self.sceneName)
        self.getFrameRange()
        if self.min != frameRange[0]:
            return False
        if self.max != frameRange[1]:
            return False
        return True

    
if __name__ == "__main__":
    a = ANIMInterceptTool()
    a.show()