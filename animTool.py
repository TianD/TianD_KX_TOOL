#coding:utf-8
'''
Created on 2015/7/8

@author: TianD
'''
import sys
path = "E:\\Scripts\\Eclipse\\TianD_KX_TOOL"
if path not in sys.path:
    sys.path.append(path)

import pymel.core as pm
import uiTool
import kxMayaTool
reload(uiTool)

class ANIMTool(kxMayaTool.KXTool):
    
    def __init__(self):
        '''
        13 动画规范拦截:
            1.相机锁定;
            2.相机缩放归1;
            3.清理除norender以外的层;
            4.清理空组;
            5.拦截cam的命名和文件命名不一样;(重要的)
            6.拦截帧数和数据库不一样;(重要的)
            7.清理多余的摄像机;
            8.自动在outerline里吧角色归到char组,场景归到set组,道具归到prop组;
        '''
        super(ANIMTool, self).__init__()
        
        
    def getAnimCamera(self):
        self.analyzeSceneName()
        if self.fileName:
            cameraName = "cam_%s_%s_%s" %(self.setNumber, self.sessionName, self.sceneName)
            try:
                self.camera = pm.PyNode(cameraName)
            except:
                return "没有正确命名的相机!!!"
        
        else :
            pass
        
    
    def getNeedlessCamera(self):
        cameraLst = [cam.getParent() for cam in pm.ls(type = 'camera')]
        self.needlessCamera = [cam for cam in cameraLst if cam not in self.defaultCameraNameLst and cam != self.camera]
        if self.needlessCamera :
            return "有多余的相机!!!"
        
    def getFileFrames(self):
        pass
    
    def camScale1(self):
        scale = self.camera.s.get()
        if scale != pm.dt.Vector([1.0, 1.0, 1.0]):
            return "相机缩放不是1!!!"
    
    def camLock(self):
        cbAttr = self.camera.listAttr(k=1) + self.camera.getShape().listAttr(k=1)
        for attr in cbAttr:
            if not attr.isLocked():
                return "相机属性没有锁定!!!"
    
 
def animIntercept():
    errorDic = dict()
    
    anim = ANIMTool()
    
    #检查相机
    result = anim.getAnimCamera()
    if result :
        errorDic[result] = None
    else :
        #获取多余相机
        result = anim.getNeedlessCamera()
        if result :
            errorDic[result] = anim.needlessCamera
        
        #相机锁定
        result = anim.camLock()
        if result :
            errorDic[result] = anim.camera
        
        #相机缩放
        result = anim.camScale1()
        if result :
            errorDic[result] = anim.camera
    
    emb = uiTool.ErrorMessageBox()
    emb.displayError(**errorDic)
    emb.show()
    
animIntercept()