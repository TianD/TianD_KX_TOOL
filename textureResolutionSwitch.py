#coding:utf-8
'''
Created on 2015年8月19日 下午1:43:29

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import pymel.core as pm

def switch(switch = 0, value = 32):
    files = pm.ls(type = "file")
    
    attrName = "resolution"
    
    for f in files:
        #switch = 0, 为贴图32位显示; switch = 1,  为默认高精度显示;
        if switch :
            if f.hasAttr(attrName):
                f.resolution.delete()
            else :
                pass
        else :
            if f.hasAttr(attrName):
                f.resolution.set(value)
            else :
                pm.addAttr(f, ln = "resolution",at ="long", dv=value)
        pm.refreshEditorTemplates()
        pm.refresh()
    pm.confirmDialog(title='Switch', message='转换完成', button = ['OK'])
    
        
if __name__ == "__mian__":
    switch(0, 64)
    switch(1)    