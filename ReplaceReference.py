#coding:utf-8
'''
Created on 2015年10月29日 上午11:24:52

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: replace low geo with high geo

@Declaration: It's free for everybody and welcome to point out mistakes.
'''
import pymel.core as pm

import lightRenderData

def startReplaceL2H():
    projDic = {
               'XFTL': ['_l_', '_h_'],
               'SENBA': ['_l_', '_h_'],
               'ROCK': ['_l_', '_h_']
                }
    fromto = []
    env = pm.Env()
    fileName = env.sceneName().namebase
    projMatch = lightRenderData.ProjNameMatch()
    projMatch.setFileName(fileName)
    projName = projMatch.getPorjName()
    if projName and projName in projDic:
        fromto = projDic[projName]
        replaceL2H(fromto[0], fromto[1])
    

def replaceL2H(fr, to):
    #把参考文件的低模, 替换成高模
    #
    #把字段f替换成t
    #
    #列出所有参考文件，存到以namespace为key的字典中
    refs = pm.system.getReferences()
    noH = []
    for key, value in refs.items():
        name_space = key
        fileRef = value
        #列出参考文件的路径和文件名
        file_path = fileRef.path
        file_name = file_path.name
        #将带'_l_'标示的低模, 替换成带'_h_'标示的高模
        if fr in file_name:
            hf = file_name.replace(fr, to)
            hd = file_path.replace(fr, to)
            dir = pm.Path(file_path).dirname()
            #如果服务器上有高模文件就进行替换, 没有就加入到一个列表里以便弹窗报错
            if hf in [f.name for f in dir.files()]:
                fileRef.replaceWith(hd)
            else :
                noH.append(file_path)
    
    if noH :
        pm.confirmDialog( title=u'提示', message='\n'.join(noH) + u'\n 没有"_h_"文件', button=[u'确认'])
    else:
        pm.confirmDialog( title=u'提示', message=u'完成', button=[u'确认'])
        

def importRef():
    refs = pm.system.getReferences()
    for key, value in refs.items():
        name_space = key
        fileRef = value
        try:
            fileRef.importContents()
        except:
            print fileRef, "import failure!!!"
            
if __name__ == "__main__":
    startReplaceL2H()