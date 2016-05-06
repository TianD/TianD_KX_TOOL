#coding:utf-8
'''
Created on 2016年4月6日 下午5:46:48

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:
'''

import re
from functools import partial

def _add1(groupName, matched):
    intStr = matched.group(groupName)
    if intStr:
        intValue = int(intStr)
    else :
        intValue = 0
    addedValue = intValue + 1
    addedValueStr = str(addedValue)
    return addedValueStr


def compileFileName(filePath):
    import os.path
    
    if not os.path.exists(filePath):
        return filePath
    pathWithoutExt, ext = os.path.splitext(filePath)
    newPathWithoutExt = re.sub("(?P<number>\d*)$", partial(_add1, 'number'), pathWithoutExt)
    newFilePath =  "{0}{1}".format(newPathWithoutExt, ext)
    return compileFileName(newFilePath)

def compileNodeName(nodeName):
    import pymel.core as pm
    
    if not pm.objExists(nodeName):
        return nodeName
    newNodeName = re.sub("(?P<number>\d*)$", partial(_add1, 'number'), nodeName)
    return compileNodeName(newNodeName)
    
if __name__ == "__main__":
    print compileFileName("E:\\test\\image\\Oceab_v3_Ocean_1001.tif")