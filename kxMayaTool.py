#coding:utf-8
'''
Created on 2015/7/7

@author: TianD
'''

import sys, os

import re, glob

class KXTool(object):
    
    def __init__(self):
        '''
                用于凯旋项目，所有TianD功能的基类
        '''
        self.excelPath = "C:\\Users\\huiguoyu\\Desktop"
        self.defaultCameraNameLst = ['persp', 'top', 'front', 'side']
        
    def analyzeSceneName(self):
        
        import pymel.core as pm
        
        self.sceneName = pm.Env().sceneName().namebase
        
        if self.fileName :
            m = re.match(r"(?P<project_name>\w+)_(?P<episode_number>\d+)_(?P<session_number>\w+)_(?P<scene_number>\d+)_(?P<process_name>\w+)_(?P<version_number>\w+)", self.fileName)
            self.projectName = m.group('project_name')              #项目名称
            self.episodeNumber =  m.group('episode_number')         #集数     
            self.sessionNumber = m.group('session_number')              #场号  
            self.sceneNumber = m.group('scene_number')                  #镜头号
            self.processName = m.group('process_name')              #环节名称
            self.versionNumber = m.group('version_number')              #版本号
        else :
            pass
        

    def getExcel(self, path = None):
        
        import excelTool
                
        if path :
            pass
        else :
            self.analyzeSceneName()
            path = glob.glob("%s\\[!~$]*%s*.xls*" %(self.excelPath, self.setNumber))
            if len(path) == 1 :
                return path[0]
            else :
                return None
        
        self.wb = excelTool.open(path)
        
    