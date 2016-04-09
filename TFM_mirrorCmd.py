#coding:gbk
import re
import pymel.core as pm
import maya.OpenMayaAnim as OpenMayaAnim
import utils

dt = {'L_':'R_', 'l_':'r_', 'left_':'right_', 'Left_':'Right_', 'R_':'L_', 'r_':'l_', 'Right_':'Left_', 'right_':'left_'}

def getMirrorCtrl(ctrl):
    ctrlName = ctrl.name()
    for key, value in dt.iteritems():
        if key in ctrlName:
            mirrorCtrlName = ctrlName.replace(key, value)
            return pm.PyNode(mirrorCtrlName)
    return ctrl

def getBoxBuffer(ctrl):
    ctrlName = ctrl.name()
    return pm.PyNode("{0}_boxBuffer".format(ctrl))
           
def getAttrDrivenCurve(driver, driverAttr, driven, drivenAttr):
    drivenCurveName = "{driver}_{driverAttr}_to_{driven}_{drivenAttr}".format(driver=driver.name(), driverAttr=driverAttr, driven=driven.name(), drivenAttr=drivenAttr)
    if pm.objExists(drivenCurveName):
        return pm.PyNode(drivenCurveName)
    else :
        return None 

def getMirrorAttrDrivenCurve(animUL):
    driverName, driverAttr, drivenName, drivenAttr = getDrivenName(animUL)
    mirrorDriver = getMirrorCtrl(pm.PyNode(driverName))
    mirrorDriven = getMirrorCtrl(pm.PyNode(drivenName))
    mirrorAnimUL = getAttrDrivenCurve(mirrorDriver, driverAttr, mirrorDriven, drivenAttr)
    if mirrorAnimUL:
        pm.delete(mirrorAnimUL)
    mirrorAnimULName = "{driver}_{driverAttr}_to_{driven}_{drivenAttr}".format(driver=mirrorDriver.name(), driverAttr=driverAttr, driven=mirrorDriven.name(), drivenAttr=drivenAttr)
    mirrorAnimUL = pm.createNode("animCurveUL", name = mirrorAnimULName)
    mfnAnimUL = mirrorAnimUL.__apimfn__()

    for i in range(animUL.numKeys()):
        input = animUL.getUnitlessInput(i)
        value = animUL.getValue(i)
        if driverAttr == 'tx' and drivenAttr == 'tx':
            if input != 0:
                newInput = -1*input
                newValue = -1*value
        elif driverAttr == 'tx' and drivenAttr != 'tx':
            if input != 0:
                newInput = -1*input
                newValue = value
        else :
            newInput = input
            newValue = value
        mfnAnimUL.addKey(newInput, newValue, 1, 1)
        
    return mirrorAnimUL

def getDrivenName(animUL):
    animULName = animUL.name()
    driverName = animULName.split('_to_')[0][:-3]
    driverAttr = animULName.split('_to_')[0][-2:]
    drivenName = animULName.split('_to_')[1][:-3]
    drivenAttr = animULName[-2:]
    return driverName, driverAttr, drivenName, drivenAttr

def mirrorDrivenCurve(driver, driverAttr, driven, drivenAttr):
    mirrorDriver = getMirrorCtrl(driver)
    mirrorDriven = getMirrorCtrl(driven)
    animUL = getAttrDrivenCurve(driver, driverAttr, driven, drivenAttr)
    if not animUL:
        return False
    mirrorAnimUL = getMirrorAttrDrivenCurve(animUL)

    pm.PyNode("%s.%s" %(mirrorDriver.name(), driverAttr)) >> mirrorAnimUL.input
    if pm.PyNode("%s.%s" %(mirrorDriven.name(), drivenAttr)).isConnected():
        source = pm.PyNode("%s.%s" %(mirrorDriven.name(), drivenAttr)).inputs()
        if source[0].type() == "blendWeighted":
            inputs = source[0].input.elements()
            nextInput = re.sub("(?P<number>\d+)", utils._add1, inputs[-1])
            mirrorAnimUL.output >> pm.PyNode("{0}.{1}".format(source[0].name(), nextInput))
            source[0].output >> pm.PyNode("%s.%s" %(mirrorDriven.name(), drivenAttr))
        elif source[0].type() == "animCurveUL":
            blendWeighted = pm.createNode("blendWeighted")
            source[0].output >> blendWeighted.input[0]
            mirrorAnimUL.output >> blendWeighted.input[1]
            blendWeighted.output >> pm.PyNode("%s.%s" %(mirrorDriven.name(), drivenAttr))
        else :
            raise "unidentifiable input connections!!!"
    else :
        mirrorAnimUL.output >> pm.PyNode("%s.%s" %(mirrorDriven.name(), drivenAttr))
    return mirrorAnimUL    
             
def setMirrorDrivenKey(ctrl, boxCtrl):
    boxBuffer = getBoxBuffer(ctrl)
    for driverAttr in ['tx', 'ty']:
        for drivenAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
            mirrorAnimUL = mirrorDrivenCurve(boxCtrl, driverAttr, boxBuffer, drivenAttr)
            
def run():
    sel = pm.ls(sl=1)
    if sel:
        setMirrorDrivenKey(sel[0], sel[1])
    else :
        raise u"请选择一个ctrl和一个boxCtrl."
if __name__ == "__main__":
    run()
    