#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 25 Jan 2016, 16:32:57
#========================================
import pymel.core
import maya.cmds as mc
import maya.OpenMaya as OpenMaya
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def setRange(oldMin, oldMax, newMin, newMax, value):
    '''
    0 - 10  --->  0 - 100
      |             |
      5      ->     50
    '''
    result = ((float(value) - oldMin) / (oldMax - oldMin) * (newMax - newMin)) + newMin
    return result




def get_nurbs_uv_at_point(surface, point=(0, 0, 0, 1.0)):
    '''
    get surface uv value by input point position...
    '''
    #- initialize
    suf_mel_node = surface
    suf_pml_node = pymel.core.PyNode(suf_mel_node)
    suf_mfn_node = OpenMaya.MFnNurbsSurface(suf_pml_node.__apiobject__())

    #- set argments
    inputPoint = OpenMaya.MPoint(*point)

    u_valueUtil, v_valueUtil = [OpenMaya.MScriptUtil() for i in range(2)]
    u_valuePtr = u_valueUtil.asDoublePtr()
    v_valuePtr = v_valueUtil.asDoublePtr()

    #- get domain values
    start_u_util, end_u_util, start_v_util, end_v_util = [OpenMaya.MScriptUtil() for i in range(4)]
    startU = start_u_util.asDoublePtr()
    endU   = end_u_util.asDoublePtr()
    startV = start_v_util.asDoublePtr()
    endV   = end_v_util.asDoublePtr()
    suf_mfn_node.getKnotDomain(startU, endU, startV, endV)

    #- config result
    closest_point = suf_mfn_node.closestPoint(inputPoint, u_valuePtr, v_valuePtr, True, 0.0001, OpenMaya.MSpace.kWorld)
    u_value = setRange(OpenMaya.MScriptUtil(startU).asDouble(), OpenMaya.MScriptUtil(endU).asDouble(), 0.0, 1.0, OpenMaya.MScriptUtil(u_valuePtr).asDouble())
    v_value = setRange(OpenMaya.MScriptUtil(startV).asDouble(), OpenMaya.MScriptUtil(endV).asDouble(), 0.0, 1.0, OpenMaya.MScriptUtil(v_valuePtr).asDouble())

    return u_value, v_value
