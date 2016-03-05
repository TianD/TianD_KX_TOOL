#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 26 Jan 2016, 16:06:57
#========================================
import pymel.core
import maya.OpenMaya as OpenMaya
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def get_polygon_uv_at_point(geometry, point=(0, 0, 0, 1.0)):
    '''
    get polygon's uv value by point...
    '''
    poly_mel_node = geometry
    poly_pml_node = pymel.core.PyNode(poly_mel_node)
    poly_mfn_node = OpenMaya.MFnMesh(poly_pml_node.__apiobject__())

    inPoint = OpenMaya.MPoint(*point)

    uv_script_util = OpenMaya.MScriptUtil()
    uv_value_ptr   = uv_script_util.asFloat2Ptr()
    poly_mfn_node.getUVAtPoint(inPoint, uv_value_ptr, OpenMaya.MSpace.kWorld)

    u_value = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_value_ptr, 0, 0)
    v_value = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_value_ptr, 0, 1)

    return u_value, v_value
