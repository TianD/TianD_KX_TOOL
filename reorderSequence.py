#coding:utf-8
'''
Created on 2015年9月8日 上午9:29:14

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import os
import re

def reorder(filePath, sequenceDict):
    separateStr = "separateFiles"
    for key, values in sequenceDict.items():
        if separateStr == key:
            pass
        else :
            try:
                formatStr = re.findall("\d+%\dd", key)[0]        # "00%2d"
            except :
                raise "nonononono"
            prefix = formatStr.split("%")[0]                     # "00%2d" --> "00"   
            length = int(formatStr.split("%")[-1][0])            # "00%2d" --> 2
            start = int(values[0])
            end = int(values[1])
            short = values[2]
            sequence = values[-1]
            ext = key.split('.')[-1]
            if not short and len(sequence) == (end - start + 1) and start != 1:                
                for i in range(end - start + 1):
                    currentindex = re.search('\d+(?=\.%s)' %ext, sequence[i]).group()
                    newindex = prefix + str(i+1).zfill(length)
                    currentname = "%s\\%s" %(filePath, sequence[i])
                    newname = currentname.replace(currentindex, newindex)
                    os.rename("%s\\%s" %(filePath, sequence[i]), newname)                     
            elif short:
                print "缺帧", short
            elif not short and len(sequence) != (end - start + 1):
                print "文件数量与帧数范围不符"
            else :
                print "已经是从1开始的序号"
            
    print "OK"
    

'''
example:

import sys

scriptpath = "E:\\Scripts\\KX\\SequenceFileDetection"

scriptpath in sys.path or sys.path.append(scriptpath)


import os
path = 'D:\\sqLR6\\sc002\\c001'

import SequenceFileDetection as sfd

files = os.listdir(path)
aa = sfd.SequenceFileDetection()
aa.setSequenceFiles(files)
tempDict = aa.getSequenceInfo(1)

reorder(path, tempDict)
'''
