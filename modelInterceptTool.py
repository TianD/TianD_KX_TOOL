#coding:utf-8
'''
Created on 2015年8月21日 下午5:02:44

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
#coding:utf-8
'''
Created on 2015/8/24

@author: TianD
'''
import os
import itertools

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
        self.setMaximumWidth(200)
        
        self.setWindowIcon(QtGui.QIcon("%s/bullet_deny.png" %uiPath))
        
        for btn in self.findChildren(QtGui.QPushButton, QtCore.QRegExp("check\d+Btn")):
            btn.setIcon(QtGui.QIcon("%s/question.png" %uiPath))
            btn.setStyleSheet('border-image:url(%s/question.png);' %uiPath)
        
        
        self.check0Btn.clicked.connect(self.modelHistory)               #物体历史
        self.check1Btn.clicked.connect(self.modelTransform)                #位移变换
        
        self.checkAllBtn.clicked.connect(self.checkAll)
        self.skipAllBtn.clicked.connect(self.skipAll)
        
        self.flag0 = None
        self.flag1 = None
        
        self.model = MODELIntercept()
        
        #self.checkAll()
                    
    def modelHistory(self):
        flag = self.model.modelHistory()
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
            pm.select(self.model.historyResult)
    
    def modelTransform(self):
        flag = self.model.modelTransform()
        if flag :
            self.check1Btn.setIcon(QtGui.QIcon("%s/ok.png" %uiPath))
            self.check1Btn.setStyleSheet("border-image:url(%s/ok.png);" %uiPath)
            self.flag1 = True
        else :
            self.check1Btn.setIcon(QtGui.QIcon("%s/cancel.png" %uiPath))
            self.check1Btn.setStyleSheet("border-image:url(%s/cancel.png);" %uiPath)
            self.flag1 = False
        if self.flag1 is True:
            pass
        else :
            pm.select(self.model.transformResult)
            
    def checkAll(self):
        if not self.skip0.checkState() :
            self.flag0 = None
            self.modelHistory()
        if not self.skip1.checkState():
            self.flag1 = None
            self.modelTransform()
            
        if (self.flag0 or self.skip0.checkState()) and \
            (self.flag1 or self.skip1.checkState()):
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
        self.topGroups = ["persp", "top", "front", "side", "char", "set", "prop"]
        self.attrLst = ["%s%s" %x for x in itertools.product("trs","xyz")]
        
    def listMesh(self):
        return pm.ls(type = "mesh")

    def listTransform(self):
        return [i for i in pm.ls(type = "transform") if i.name() not in self.topGroups]
        
    def modelHistory(self, mesh = None):
        self.historyResult = []
        if not mesh:
            mesh = self.listMesh()
        for i in mesh:
            if not i.isIntermediate():
                if i.listHistory():
                    if len(i.listHistory()) == 1 and i.listHistory()[0] == i:
                        pass
                    else :
                        if i not in self.historyResult:
                            self.historyResult.append(i.name())
        if self.historyResult :
            return False
        else :
            return True
    
    def modelTransform(self, transform = None):
        self.transformResult = []
        if not transform:
            transform = self.listTransform()
        for i in transform:
            for attr in self.attrLst:
                if "s" not in attr:
                    if i.getAttr(attr) != 0:
                        if i not in self.transformResult:
                            self.transformResult.append(i.name())
                            break
                else :
                    if i.getAttr(attr) != 1:
                        if i not in self.transformResult:
                            self.transformResult.append(i.name())
                            break
        if self.transformResult:
            return False
        else :
            return True
                    
def show():
    if uiTool.windowExisted("modelInterceptWindow"):
        return uiTool.toQtObject("modelInterceptWindow")
    else :
        a = MODELInterceptTool()
        a.show()
        return uiTool.toQtObject("modelInterceptWindow")
      
if __name__ == "__main__":
    show()