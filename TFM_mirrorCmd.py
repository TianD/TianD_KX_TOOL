#coding:gbk
import re
import pymel.core as pm

ldt = {'L_':'R_', 'l_':'r_', 'left_':'right_', 'Left_':'Right_'}

rdt = {'R_':'L_', 'r_':'l_', 'Right_':'Left_', 'right_':'left_'}

def getMirrorCtrl(ctrl):
    ctrlName = ctrl.name()
    mirrorCtrlName = ctrlName
    flag = 0
    for s, r in ldt.iteritems():
        res = re.search(s, mirrorCtrlName)
        if not res:
            continue
        if res.start() != 0 and mirrorCtrlName[res.start()-1] != '_':
            continue
        mirrorCtrlName = mirrorCtrlName[:res.start()] + r + mirrorCtrlName[res.end():]
        flag += 1
        
    if not flag :
        for s, r in rdt.iteritems():
            res = re.search(s, mirrorCtrlName)
            if not res:
                continue
            if res.start() != 0 and mirrorCtrlName[res.start()-1] != '_':
                continue
            mirrorCtrlName = mirrorCtrlName[:res.start()] + r + mirrorCtrlName[res.end():]
    
    if pm.objExists(mirrorCtrlName):
        return pm.PyNode(mirrorCtrlName)
    else:
        return pm.duplicate(ctrl, name = mirrorCtrlName)[0]

# def getMirrorCtrl(ctrl):
#     ctrlName = ctrl.name()
#     mirrorCtrlName = ctrlName
#     if 'L_' in mirrorCtrlName or 'l_' in mirrorCtrlName:
#         mirrorCtrlName = mirrorCtrlName.replace('L_', 'R_').replace('l_', 'r_')
#     elif 'R_' in mirrorCtrlName or 'r_' in mirrorCtrlName:
#         mirrorCtrlName = mirrorCtrlName.replace('R_', 'L_').replace('r_', 'l_')
#     if 'Left_' in mirrorCtrlName or 'left_' in mirrorCtrlName:
#         mirrorCtrlName = mirrorCtrlName.replace('Left_', 'Right_').replace('left_', 'right_')
#     elif 'Right_' in mirrorCtrlName or 'right_' in mirrorCtrlName:
#         mirrorCtrlName = mirrorCtrlName.replace('Right_', 'Left_').replace('right_', 'left_')
#     
#     if pm.objExists(mirrorCtrlName):
#         return pm.PyNode(mirrorCtrlName)
#     else:
#         return pm.duplicate(ctrl, name = mirrorCtrlName)[0]
           
def getDriver(ctrl):
    boxBuffer = pm.PyNode('%s_boxBuffer' %ctrl.name()) 
    animUL = []
    getAttrDrivenCurve(boxBuffer.tx, animUL)
    getAttrDrivenCurve(boxBuffer.ty, animUL)
    getAttrDrivenCurve(boxBuffer.tz, animUL)
    boxControlName = animUL[0].split('tx')[0].split('ty')[0]
    return pm.PyNode(boxControlName[:-1]), animUL
    
def getAttrDrivenCurve(thisNode, result = []):
    for node in thisNode.inputs(scn=1):
        if node.type() == 'animCurveUL' and node not in result:
            result.append(node)
        getAttrDrivenCurve(node, result)
    return result
        
def getDrivenName(animUL):
    animULName = animUL.name()
    driverName = animULName.split('_to_')[0][:-3]
    driverAttr = animULName.split('_to_')[0][-2:]
    drivenName = animULName.split('_to_')[1][:-3]
    drivenAttr = animULName[-2:]
    return driverName, driverAttr, drivenName, drivenAttr

def mirrorDrivenCurve(animUL):
    mirrorAnimUL = getMirrorCtrl(animUL)
    driverName, driverAttr, drivenName, drivenAttr = getDrivenName(mirrorAnimUL)
    if driverAttr == 'tx':
        for i in range(animUL.numKeys()):
            value = animUL.getValue(animUL.numKeys() - i - 1)
            mirrorAnimUL.setValue(i, value)
    if drivenAttr == 'tx':
        for i in range(mirrorAnimUL.numKeys()):
            value = mirrorAnimUL.getValue(i)
            mirrorAnimUL.setValue(i, -1 * value)
    pm.PyNode("%s.%s" %(driverName, driverAttr)) >> mirrorAnimUL.input
    try:
        mirrorAnimUL.output >> pm.PyNode("%s.%s" %(drivenName, drivenAttr))
    except:
        pass
    return mirrorAnimUL    
    
def blendCurve(animUL1, animUL2):
    driverName1, driverAttr1, drivenName1, drivenAttr1 = getDrivenName(animUL1)
    driverName2, driverAttr2, drivenName2, drivenAttr2 = getDrivenName(animUL2)
    if driverName1 == driverName2 and drivenName1 == drivenName2 and drivenAttr1 == drivenAttr2:
        blendNode = pm.createNode("blendWeighted")
        animUL1.output >> blendNode.input[0]
        animUL2.output >> blendNode.input[1]
        blendNode.output >> pm.PyNode("%s.%s" %(drivenName1, drivenAttr1))
    else :
        print u"{0},{1}驱动的不是同一个属性, 或者不是被同一个节点驱动.".format(animUL1.name(), animUL2.name())
        
def setMirrorDrivenKey(ctrl):
    mirrorCtrl = getMirrorCtrl(ctrl)
    boxCtrl, animULs = getDriver(ctrl)
    mirrorBoxCtrl = getMirrorCtrl(boxCtrl)
    blendGroup = dict()
    for animUL in animULs:
        mirrorAnimUL = mirrorDrivenCurve(animUL)
        driverName, driverAttr, drivenName, drivenAttr = getDrivenName(mirrorAnimUL)
        blendGroup.setdefault(drivenAttr, list()).append(mirrorAnimUL)
        
    for key, value in blendGroup.items():
        if len(value) > 1 :
            blendCurve(value[0], value[1])

def run():
    sel = pm.ls(sl=1)
    if sel:
        setMirrorDrivenKey(sel[0])
    else :
        raise u"请选择一个控制器."
if __name__ == "__main__":
    run()
    