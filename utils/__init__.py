#coding:utf-8
'''
Created on 2016年3月2日 下午4:34:53

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:
'''

import re

def _add1(matched):
    intStr = matched.group("number")
    intValue = int(intStr)
    addedValue = intValue + 1
    addedValueStr = str(addedValue)
    return addedValueStr