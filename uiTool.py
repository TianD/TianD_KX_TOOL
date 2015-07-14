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

def getChildrenUI(uiObject):
    return uiObject.children()

def windowExisted(mayaName):
    uiObject = toQtObject(mayaName)
    if uiObject :
        uiObject.showNormal()
        uiObject.activateWindow()
        return True
    else :
        return False