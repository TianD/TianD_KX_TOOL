#coding:utf-8
'''
Created on 2015/7/7

@author: TianD
'''

import sys, os

import re, glob

import pymel.core as pm

class KXTool(object):
    
    def __init__(self):
        '''
                用于凯旋项目，所有MAYA内部功能的基类
        '''
        self.projectPath = "C:\\Users\\huiguoyu\\Desktop"
        self.defaultCameraNameLst = ['persp', 'top', 'front', 'side']
        self.fileName = pm.Env().sceneName().namebase

    def analyzeSceneName(self):
        if self.fileName :
            m = re.match(r"(?P<project_name>\w+)_(?P<set_number>\d+)_(?P<session_name>\w+)_(?P<scene_name>\d+)_(?P<process_name>\w+)_(?P<version_name>\w+)", self.fileName)
            self.projectName = m.group('project_name')      #项目名称
            self.setNumber =  m.group('set_number')         #集数     
            self.sessionName = m.group('session_name')      #场号  
            self.sceneName = m.group('scene_name')          #镜头号
            self.processName = m.group('process_name')      #环节名称
            self.versionName = m.group('version_name')      #版本号
        else :
            pass
        
        