#coding:utf-8
'''
Created on 2015/7/10

@author: TianD
'''

import xlrd

class EXCELRead(object):
    
    def __init__(self, path):
        '''
                读取excel表格的类
                分析sheet, row, col, header, cell等内容
        header包括: 集数, 场次, 镜头号, 帧数, 起始, 结束, upload, 夸张表情, 罐头镜, 特效清单
        '''
        try:
            wb = xlrd.open_workbook(path)
        except Exception,e:
            print str(e)
            
        self.sheet = wb.sheets()[0]
        
        self.__analyzeHeader()
    
    def __analyzeHeader(self):
        headers = self.sheet.row_values(0)
        self.head_episode = headers[0]
        self.head_session = headers[1]
        self.head_scene = headers[2]
        self.head_frames = headers[3]
        self.head_start = headers[4]
        self.head_end = headers[5]
        return headers
    
    #def getFrames(sheet, episodeNumber, sessionNumber, sceneNumber):
        
    def locate(self):
        self.sheet.col_values()
    