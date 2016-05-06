#coding:utf-8
'''
Created on 2016年3月29日 上午10:14:41

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: 1.Export; 2. Simulation; 3.Import; 4.BCT
'''
import os.path
import pymel.core as pm
import kxTool
import utils.cache as cache
import utils.name as name

def showUI():
    with pm.window('KX_ClothING', title = 'KX_Clothing') as win:
        with pm.rowColumnLayout('mainLayout', numberOfColumns = 2) as mainLayout:
            selectBtn = pm.button(label = u'添加要导出的模型', c = selectCmd)
            exportBtn = pm.button(label = u'导出并创建解算场景', c = exportCmd)
            nClothBtn = pm.button(label = u'创建NCloth布料', c = nClothCmd)
            qClothBtn = pm.button(label = u'创建QCloth布料', c = qClothCmd)
            paintBtn = pm.button(label = u'调整动画权重', c = paintCmd)
            createBtn = pm.button(label = u'生成布料缓存', c = createCmd)
            importBtn = pm.button(label = u'导入布料缓存', c = importCmd)
            bctBtn = pm.button(label = u'布料修穿工具', c = bctCmd)
           
    win.show()
    
def selectCmd(*args, **kwargs):
    '''
    add selection model into the display layer
    '''
    exportLayerName = 'kx_cloth_export_layer'
    if pm.objExists(exportLayerName):
        exportLayer = pm.PyNode(exportLayerName)
    else :
        exportLayer = pm.createDisplayLayer(noRecurse = 1, e = 1, name = 'kx_cloth_export_layer')
    exportLayer.visibility.set(0)
    exportLayer.color.set(14)
    
    sel = pm.ls(sl=1)
    exportLayer.addMembers(sel)
    return exportLayerName
    
def exportCmd(*args, **kwargs):
    '''
    export models with animation
    '''
    kx = kxTool.KXTool()
    kx.getSceneName()
    sceneName = kx.sceneName
    scenePath = kx.scenePath
    
    cachePath = "{path}/{name}/{name}_cloth.abc".format(path = scenePath.replace('scenes', 'cache/alembic'), name = sceneName)
    cacheFile = name.compileFileName(cachePath)
    fileName = name.compileFileName("{path}/{name}_cloth.mb".format(path = scenePath, name = sceneName))
    
    geos = pm.PyNode('kx_cloth_export_layer').listMembers()
    exportGeos = []
    for geo in geos: 
        dup = pm.duplicate(geo, name = '{0}_toCloth'.format(geo.name()))[0]
        dup.setParent(w=1)
        shapes = dup.getShapes()
        pm.delete(shapes[1:])
        pm.blendShape(geo, dup, o = 'world', w = (0,1))
        exportGeos.append(dup)
    
    cache.exportAbcCache(exportGeos, cacheFile, useTimeline = True, verbose = True)
    
    pm.newFile(f=1)
    
    sourceGrp = pm.createNode('transform', name = 'source_Grp')
    
    abcNodeName = cache.importAbcCache(cacheFile)
    
    objs = pm.PyNode(abcNodeName).outputs()
        
    for obj in objs:
        obj.rename(obj.name().replace('_toCloth', '_anim'))
        obj.setParent(sourceGrp)
                    
    pm.saveAs(fileName, f=1)
    
    return fileName
    
def nClothCmd(*args, **kwargs):
    '''
    create nCloth
    
    step 1: Select an anim geo
    step 2: Duplicate a cloth geo and a output geo from the anim geo
    step 3: Do blendshape both anim geo and cloth geo with output geo
    step 4: Create NCloth on cloth geo
    '''
    
    sel = pm.ls(sl=1)
    
    outputGrpName = 'output_Grp'
    
    clothGrpName = 'cloth_Grp'
    
    if pm.objExists(outputGrpName):
        outputGrp = pm.PyNode(outputGrpName)
    else :
        outputGrp = pm.createNode('transform', name = outputGrpName)
    
    outputGrp.v.set(0)
    
    if pm.objExists(clothGrpName):
        clothGrp = pm.PyNode(clothGrpName)
    else :
        clothGrp = pm.createNode('transform', name = clothGrpName)

    clothGeos = [pm.duplicate(i, name = i.name().replace("_anim", "_cloth"))[0] for i in sel]
    
    [clothGeo.setParent(clothGrp) for clothGeo in clothGeos]
        
    outputGeos = [pm.duplicate(i, name = i.name().replace("_anim", "_output"))[0] for i in sel]
    
    [outputGeo.setParent(outputGrp) for outputGeo in outputGeos]
    
    [i.v.set(0) for i in sel]
            
    pm.select(clothGeos)
    
    clothShape = pm.mel.createNCloth(0)
    
    blendNodes = [pm.blendShape(sel[i], clothGeos[i], outputGeos[i], w = [(0,0), (1,1)]) for i in range(len(sel))]
        
def qClothCmd(*args, **kwargs):
    '''
    create qCloth
    
    step 1: Select an anim geo
    step 2: Duplicate a cloth geo and a output geo from the anim geo
    step 3: Do blendshape both anim geo and cloth geo with output geo
    step 4: Create QCloth on cloth geo
    '''
    
    try:
        pm.loadPlugin("qualoth-2014-x64.mll")
    except:
        pass
    
    sel = pm.ls(sl=1)
    
    outputGrpName = 'output_Grp'
    
    clothGrpName = 'cloth_Grp'
    
    if pm.objExists(outputGrpName):
        outputGrp = pm.PyNode(outputGrpName)
    else :
        outputGrp = pm.createNode('transform', name = outputGrpName)
    
    outputGrp.v.set(0)
    
    if pm.objExists(clothGrpName):
        clothGrp = pm.PyNode(clothGrpName)
    else :
        clothGrp = pm.createNode('transform', name = clothGrpName)
        
    outputGeos = [pm.duplicate(i, name = i.name().replace("_anim", "_output"))[0] for i in sel]
    
    [outputGeo.setParent(outputGrp) for outputGeo in outputGeos]
    
    [i.v.set(0) for i in sel]
    
    clothShape = []
    for i in sel:
        pm.select(i)
        clothShape.append(pm.mel.qlCreateCloth())
    
    clothGeos = [pm.PyNode(i).outputMesh.outputs(p=0)[0] for i in clothShape]
    
    [clothGeo.setParent(clothGrp) for clothGeo in clothGeos]
    
    blendNodes = [pm.blendShape(sel[i], clothGeos[i], outputGeos[i], w = [(0,0), (1,1)]) for i in range(len(sel))]
    

def createCmd(*args, **kwargs):
    '''
    create cloth geometry cache
    '''
    kx = kxTool.KXTool()
    kx.getSceneName()
    sceneName = kx.sceneName
    scenePath = kx.scenePath
    
    outputGrpName = 'output_Grp'
    
    if pm.objExists(outputGrpName):
        outputGrp = pm.PyNode(outputGrpName)
    else :
        pm.error("Maya Node does not exist: {0}".format(outputGrpName))
        
    outputGeos = outputGrp.getChildren()
    
    for geo in outputGeos:
        cacheFile = "{path}/{scene}/{name}.mcc".format(path = scenePath.replace('scene', 'cache/nCache'), scene = sceneName, name = geo.name())
        cache.exportMCCache(geo, cacheFile)
        cache.importMCCache(geo, cacheFile)

def importCmd(*args, **kwargs):
    '''
    import cache to original file
    step 1: find geometry cache for cloth geo
    step 2: open original anim file
    step 3: import the geometry cache to geos which export to cloth
    '''
    print 'importCmd'

    

def paintCmd(*args, **kwargs):
    '''
    paint blendshape weight
    '''
    print 'paintCmd'

def bctCmd(*args, **kwargs):
    '''
    run BCT
    '''
    import BeautifyClothTool as BCT
    reload(BCT)
    BCT.run()  
    
if __name__ == "__main__":
    showUI()