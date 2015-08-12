#coding:utf-8
'''
Created on 2015年8月10日 下午3:16:01

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
from functools import partial

from PyQt4 import QtGui
import pymel.core as pm

import kxTool, uiTool

def getFileNode():
    fileNodes = []
    sel = pm.ls(sl=1)
    for sl in sel:
        shape = sl.getShape()
        sg = shape.outputs(type = "shadingEngine")[0]
        shader = sg.surfaceShader.inputs()[0]
        file = shader.color.inputs(type = "file")
        if file :
            if file[0] not in fileNodes:
                fileNodes.append(file[0])
    return fileNodes

def getImagePath(fileNode):
    if type(fileNode) == "str":
        filePath = pm.PyNode(fileNode).fileTextureName.get()
    else:
        filePath = fileNode.fileTextureName.get()
    return filePath

def setNewPath(filePath, localdir, addition):
    name = pm.Path(filePath).namebase
    base = pm.Path(filePath).splitext()[0]
    ext = pm.Path(filePath).splitext()[-1]
    prefix = base.split("/sourceimages/")[-1].split(name)[0]
    if not pm.Path(localdir + 'sourceimages/' + prefix).exists():
        pm.Path(localdir + 'sourceimages/' + prefix).makedirs()
    newPath = localdir + 'sourceimages/' + prefix + name + addition + ext
    return newPath

def scaledImage(fileNode, filePath, newPath, percent = 0.5):
    pixmap = QtGui.QPixmap(filePath)
    newpix = pixmap.scaled(pixmap.width()*percent, pixmap.height()*percent)
    newpix.save(newPath)
    return newPath

def replaceImage(fileNode, newPath):
    fileNode.fileTextureName.set(newPath)
    print newPath
    return True

def doScale(percent, *args, **kwargs):
    files = getFileNode()
    workspace = kxTool.KXTool().getPorjPath()
    
    percent = percent
    scaled = "_scale_to_%s" %percent
    for f in files:
        imagePath = getImagePath(f)
        if imagePath:
            newPath = setNewPath(imagePath, workspace, scaled)
            scaledImage(f, imagePath, newPath, percent)
            replaceImage(f, newPath)
            
    messageBox = QtGui.QMessageBox(uiTool.getMayaWindow())
    messageBox.setText(u"所选物体的贴图以转换成0.5倍尺寸")
    messageBox.show()
    if pm.window("scaleImageTool", ex = 1):
        pm.deleteUI("scaleImageTool")
            
def showUI():
    
    with pm.window("scaleImageTool", title = u"将选中模型的贴图进行缩放,并存放在本地工程目录") as win:
        with pm.columnLayout():
            pm.floatSliderButtonGrp('fsbg', label = u"长宽缩放比例:", field= 1, buttonLabel = "go", min = 0.1, max = 1.0, v = 0.5, bc = lambda: doScale(pm.floatSliderButtonGrp('fsbg', q=1, v=1)))
    pm.showWindow(win)
    
    
if __name__ == "__main__":
    showUI()