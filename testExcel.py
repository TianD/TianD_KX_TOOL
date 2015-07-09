#coding:utf-8
'''
Created on 2015/7/8

@author: TianD
'''

from xlrd import open_workbook

wb = open_workbook(u"C:\\Users\\huiguoyu\\Desktop\\EP019帧数表.xlsx")

for s in wb.sheets():
    print "Sheet:", s.name
    for col in range(s.ncols):
        print s.cell(0,col).value
    
    for row in range(s.nrows):
        print s.cell(row,0)
        
    