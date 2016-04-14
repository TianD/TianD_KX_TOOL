#coding:utf-8
'''
Created on 2016年2月17日 下午4:05:23

@author: TianD 

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import pymel.core as pm
  
def toVertex(selection):
    objects = set()
    for sel in selection:
        if isinstance(sel, pm.general.MeshFace):
            objects |= set([pm.PyNode('{0}.vtx[{1}]'.format(sel.node().name(), i)) for i in sel.getVertices()])
        elif isinstance(sel, pm.general.MeshEdge):
            objects |= set(sel.connectedVertices())
        elif isinstance(sel, pm.general.MeshVertex):
            objects.add(sel)
        elif isinstance(sel, pm.nodetypes.Mesh):
            objects |= set(sel.vtx)
        elif isinstance(sel, pm.nodetypes.Transform):
            if isinstance(sel.getShape(), pm.nodetypes.Mesh):
                objects |= set(sel.vtx)
            else :
                print "{0}has no MeshVertex".format(sel.name())
        else :
            print "{0}has no MeshVertex".format(sel.name())
    return list(objects)

def toShape(selection):
    objects = set()
    for sel in selection:
        if isinstance(sel, pm.nodetypes.Mesh) or isinstance(sel, pm.nodetypes.NurbsSurface):
            objects.add(sel)