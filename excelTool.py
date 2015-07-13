#coding:utf-8
'''
Created on 2015/7/10

@author: TianD
'''

import xlrd

'''
读取excel表格的类
分析sheet, row, col, header, cell等内容
header包括: 集数, 场次, 镜头号, 帧数, 起始, 结束, upload, 夸张表情, 罐头镜, 特效清单
'''

def openExcel(path):
    try:
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        return sheet 
    except Exception,e:
        print str(e)
    
def locate(sheet, session, scene, episode = "current"):
    
    #locate scene number
    sceneLst = sheet.col_values(2)
    scene_location = [i for i in range(len(sceneLst)) if sceneLst[i] == scene]
    
    #locate session number
    sessionLst = sheet.col_values(1)
    session_location = [i for i in range(len(sessionLst)) if sessionLst[i] == session]
    
    row_number = [r for r in scene_location if r in session_location]
    
    return row_number

def getFrameRange(sheet, row):
    frames, start, end = [sheet.cell_value(row, i) for i in range(3,6)]
    return frames, start, end

if __name__ == "__main__":
    sheet = openExcel(u"C:\\Users\\huiguoyu\\Desktop\\EP019帧数表.xlsx")
    row = locate(sheet, "001", "020")
    print getFrameRange(sheet, row[0])