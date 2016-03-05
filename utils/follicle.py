#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 25 Jan 2016, 10:48:25
#========================================
import maya.cmds as mc
import nurbs, polygon
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#- Hair can only be created on NURBS or polygon surfaces.

def connect_follicle_nurbs(follicle, surface_geo):
    '''
    connect follicle and nurbs surface...
    '''
    mc.connectAttr('{0}.l'.format(surface_geo),     '{0}.is'.format(follicle),  f=True)
    mc.connectAttr('{0}.wm[0]'.format(surface_geo), '{0}.iwm'.format(follicle), f=True)

    return True




def connect_follicle_polygon(follicle, poly_geo):
    '''
    connect follicle and polygon surface...
    '''
    mc.connectAttr('{0}.o'.format(poly_geo),  '{0}.inm'.format(follicle), f=True)
    mc.connectAttr('{0}.wm'.format(poly_geo), '{0}.iwm'.format(follicle), f=True)

    return True




def connect_follicle_transform(follicle):
    '''
    connect follicle and transform translate, rotate...
    '''
    mc.connectAttr('{0}.ot'.format(follicle), '{0}.t'.format(follicle), f=True, l=True)
    mc.connectAttr('{0}.or'.format(follicle), '{0}.r'.format(follicle), f=True, l=True)

    return True




def set_follicle_parameter(follicle, u_value, v_value):
    '''
    set follicle parameter values...
    '''
    mc.setAttr('{0}.pu'.format(follicle), u_value)
    mc.setAttr('{0}.pv'.format(follicle), v_value)

    return True




def create_follicle_by_position(geometry, position=(0, 0, 0)):
    '''
    create a follicle and atach to geometry by input position...
    '''
    #- initialize...
    follicle_shape  = mc.createNode('follicle')
    follicle        = mc.listRelatives(follicle_shape, p=True, path=True)[0]
    geo_shape       = mc.listRelatives(geometry,       s=True, path=True)[0]

    #- attach to plane...
    connect_follicle_transform(follicle)
    if mc.nodeType(geo_shape) == 'mesh':
        connect_follicle_polygon(follicle, geometry)
    else:
        connect_follicle_nurbs(follicle, geometry)

    #- move follicle to given position...
    if mc.nodeType(geo_shape) == 'mesh':
        u_value, v_value = polygon.get_polygon_uv_at_point(geometry, position)
    else:
        u_value, v_value = nurbsSurface.get_nurbs_uv_at_point(geometry, position)
    set_follicle_parameter(follicle, u_value, v_value)

    return follicle




def replace_follicle_atcach_geometry(follicle, new_geo):
    '''
    connect follicle to new face...
    '''
    position  = mc.xform(follicle, q=True, ws=True, t=True)
    geo_shape = mc.listRelatives(new_geo, s=True, path=True)[0]

    #- disconnect old connect...
    for attr in ('is', 'inm', 'iwm'):
        source_attr = mc.connectionInfo('{0}.{1}'.format(follicle, attr), sfd=True)
        if source_attr:
            mc.disconnectAttr(source_attr, '{0}.{1}'.format(follicle, attr))

    #- set new UV parameters...
    if mc.nodeType(geo_shape) == 'mesh':
        u_value, v_value = polygon.get_polygon_uv_at_point(new_geo, position)
    else:
        u_value, v_value = nurbsSurface.get_nurbs_uv_at_point(new_geo, position)
    set_follicle_parameter(follicle, u_value, v_value)

    #- connect geometry...
    if mc.nodeType(geo_shape) == 'mesh':
        connect_follicle_polygon(follicle, new_geo)
    else:
        connect_follicle_nurbs(follicle, new_geo)

    return True
