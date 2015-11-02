#coding:utf-8
'''
Created on 2015年11月2日 下午4:04:13

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import maya.cmds as cmds

import lightRenderData

def startRenderTool():
    
    renderDic = {
                 'XFTL':    "import maya.mel as mel; mel.eval('lightRendering();')", 
                 'SENBA':   "from arnold_tool import showUI;win = showUI.ArnoldTool();win.show()"
                 }
    fileName = cmds.file(query=True, sceneName=True, shortName=True)
    projMatch = lightRenderData.ProjNameMatch()
    projMatch.setFileName(fileName)
    projName = projMatch.getPorjName()
    if projName and projName in renderDic:
        cmd = renderDic[projName]
    else :
        cmd = renderDic['XFTL']
    exec(cmd)