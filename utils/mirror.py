#coding:utf-8
'''
Created on 2016年3月15日 下午2:46:31

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:
'''

import pymel.core as pm
import re

mirrorDic = {'^L_':'R_', '^l_':'r_', '^left_':'right_', '^Left_':'Right_', '_L':'_R', '_l':'_r', '_LU_':'_RU_', '_LD_':'_RD_', \
             '^R_':'^L_', '^r_':'l_', '^Right_':'Left_', '^right_':'left_', '_R':'_L', '_r':'_l', '_RU_':'_LU_', '_RD_':'_LD_'}

def getMirror(object):
    if isinstance(object, basestring):
        objectName = object
    else :
        objectName = object.name()
    for key, value in mirrorDic.iteritems():
        if key in objectName:
            #mirrorObjectName = objectName.replace(key, value)
            mirrorObjectName = re.sub(key, value, objectName)
            return mirrorObjectName
    return objectName