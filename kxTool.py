#coding:utf-8
'''
Created on 2015/7/7

@author: TianD
'''

import sys, os

import re, glob

import lightRenderData as lRD

class KXTool(object):

    def __init__(self):
        '''
                用于凯旋项目，所有TianD功能的基类
        '''
        self.excelPath = "C:\\Users\\huiguoyu\\Desktop"
        self.defaultCameraNameLst = ['persp', 'top', 'front', 'side']
        self.sceneName = ''
        self.interpreter = sys.executable
        
    def getSceneName(self):
        if "Nuke" in self.interpreter:
            import nuke
            root = nuke.toNode("root")
            self.sceneName = root.name().split("/")[-1].split(".")[0]
        elif "maya" in self.interpreter:
            import pymel.core as pm
            self.sceneName = pm.Env().sceneName().namebase
            self.ext = pm.Env().sceneName().ext
        else :
            pass
        
    def analyzeSceneName_old(self):

        if self.sceneName :
            m = re.match(r"(?P<project_name>\w+)_(?P<episode_number>\d+)_(?P<session_number>\w+[a-z]{0,2})_(?P<scene_number>\d+[a-z]{0,2})_(?P<process_name>\w+)", self.sceneName)
            if m:
                self.projectName = m.group('project_name')                         #项目名称
                self.episodeNumber =  m.group('episode_number')                    #集数
                self.sessionNumber = m.group('session_number')                     #场号
                self.sceneNumber = m.group('scene_number')                         #镜头号
                self.processName = m.group('process_name').split("_")[0]           #环节版本
                self.versionNumber = m.group('process_name').split("_")[-1]         #版本号

        else :
            pass

    def analyzeSceneName(self):

        if self.sceneName :
            nameMatch = lRD.ProjNameMatch()
            nameMatch.setFileName(self.sceneName)
            nameMatch.getResults()
            self.projectName = nameMatch.getResults('project_name')                         #项目名称
            self.episodeNumber =  nameMatch.getResults('episode_number')                    #集数
            self.sessionNumber = nameMatch.getResults('session_number')                     #场号
            self.sceneNumber = nameMatch.getResults('scene_number')                         #镜头号
            self.processName = nameMatch.getResults('process_name')        #环节版本
            self.versionNumber = nameMatch.getResults('version_number')
            self.sceneDescribe = nameMatch.getResults('scene_describe')
        else :
            pass

    def getPorjPath(self):
        # get maya project
        if "maya" in self.interpreter:
            import pymel.core as pm
            return pm.workspace(q=1, dir=1)
        
    def getExcel(self, path = None):

        if path :
            pass
        else :
            self.analyzeSceneName()
            self.path = glob.glob("%s\\[!~$]*%s*.xls*" %(self.excelPath, self.episodeNumber))

