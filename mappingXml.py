#coding:utf-8
'''
Created on 2015年9月14日 下午4:22:29

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import xml.etree.cElementTree as ET

def createXML(**kwargs):
    root = ET.Element("root")
    tab1 = ET.SubElement(root, "tab", category = "tab1")
    tab2 = ET.SubElement(root, "tab", category = "tab2")
    
    btn1 = ET.SubElement(tab1, "button", name = "button1", path = "e:\\", icon = "btn1.png", input = 'print "btn1"')
    
    btn2 = ET.SubElement(tab1, "button", name = "button2", path = "e:\\", icon = "btn2.png", input = 'print "btn2"')
    
    tree = ET.ElementTree(root)  
    file = "e:\\mapping.xml"
    tree.write(file)
    
    return tree, file  

def parseXML(file, regex):
    tree = ET.ElementTree(file = file)
    result = []
    for element in tree.findall(regex):
        result.append(element.attrib)
    return result

def modifyXML(file, type, elementDic):
    tree = ET.ElementTree(file = file)
    root = tree.getroot()
    try:
        tab = tree.iterfind(elementDic['parent'])
        for i in tab:
            print i
    except:
        return False
    e = ET.SubElement(tab, type, name = elementDic['name'], path = elementDic['path'], icon = elementDic['icon'], input = elementDic['input'])
    tree.write(file)
    return True
    
if __name__ == "__main__":
    createXML()
    print parseXML("e:\\mapping.xml", "tab/button")
    edic = {"parent":'branch[@category="tab1"]', "name":"button3", "path":"e:\\", "icon":"btn3.png","input":'print "btn3"'}
    modifyXML("e:\\mapping.xml","button", edic)
    