#coding:utf-8
'''
Created on 2015年7月7日

@author: TianD
'''

import maya.OpenMayaUI as OpenMayaUI
from PyQt4 import QtGui, QtCore, uic
import sip

def wrapInstance(SwigObject):
    return sip.wrapinstance(long(SwigObject), QtCore.QObject)

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(ptr)

def toQtObject(mayaName):
    """
    Convert a Maya ui path to a Qt object
    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    @return: PyQt representation of that object
    """
    ptr = OpenMayaUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findWindow(mayaName)
    if ptr is not None:
        return wrapInstance(ptr)

def getChildrenUI(QtGuiObject):
    return QtGuiObject.children()       

uiPath = "E:\\Scripts\\Eclipse\\TianD_KX_TOOL\\source"
form_class, base_class = uic.loadUiType('%s\\errorMessageBox.ui' %uiPath)
class ErrorMessageBox(form_class, base_class):
    
    def __init__(self, parent = getMayaWindow()):
                
        super(ErrorMessageBox, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("%s\\bullet_deny.png" %uiPath))
    
    def displayError(self, **error):
        message_x_base = 120
        message_y_base = 20
        icon_x_base = 70
        icon_y_base = 20
        space = 36
        
        for i in range(len(error.keys())):
            self.addErrorMessage(message_x_base, message_y_base+i*space, icon_x_base, icon_y_base+i*space, error.keys()[i], error[error.keys()[i]])

        self.pushButton.setGeometry(QtCore.QRect(60,60+len(error)*space,200,40))
        self.resize(320, 120+len(error)*space)
        self.setMinimumSize(QtCore.QSize(320, 120+len(error)*space))
        self.setMaximumSize(QtCore.QSize(320, 120+len(error)*space))
        
    def addErrorMessage(self, mx, my, ix, iy, *args):
        message = ActiveLabel(unicode(args[0], "gbk"), parent = self)
        messageFont = QtGui.QFont()
        messageFont.setBold(1)
        messageFont.setPointSize(12)
        message.setFont(messageFont)
        message.getResult(args[1])
        icon = ActiveLabel(parent = self)
        pixmap = QtGui.QPixmap("%s\\bullet_deny24.png" %uiPath)
        icon.setPixmap(pixmap)
        message.setGeometry(QtCore.QRect(mx, my, 200, 31))
        icon.setGeometry(QtCore.QRect(ix, iy, 32, 32))
        icon.getResult(args[1])
        message.setToolTip(unicode("点击鼠标选中错误对象", "utf-8"))
        icon.setToolTip(unicode("点击鼠标选中错误对象", "utf-8"))

class ActiveLabel(QtGui.QLabel):
              
    def getResult(self, result):
        self.result = result
    
    #重写QtGui.QLabel的mousePressEvent方法, 让他选择maya中的对象       
    def mousePressEvent(self, *args, **kwargs):
        
        import pymel.core as pm
        pm.select(self.result)
            

if __name__ == "__main__":
    emb = ErrorMessageBox()
    a = {"你好":"1","不好":"2","再见":"2"}
    emb.displayError(**a)
    emb.show()