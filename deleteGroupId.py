#coding:utf-8
'''
Created on 2015年9月10日 上午9:49:03

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import pymel.core as pm
from modelInterceptTool import MODELIntercept

def delGroupId():
    model = MODELIntercept()

    model.modelHistory()

    for name in model.historyResult:
        
        shape = pm.PyNode(name)
        
        historyLst = shape.listHistory()
        
        if len(historyLst) == 1 and historyLst[0] == shape:
            pass
        else :
            sg = [h for h in historyLst if h.type() == "shadingEngine"]
            if len(sg) == 1:
                shaderLst = sg[0].surfaceShader.inputs()
                if shaderLst:
                    try:
                        outAttrLst = shape.outputs(type = "shadingEngine", c = 1, p = 1)
                        osattr = outAttrLst[0][0]
                        odattr = outAttrLst[0][1]
                        newattr = pm.PyNode(".".join(osattr.name().split(".")[:-1]))
                        newattr >> odattr
                    except:
                        pass
                    inAttrLst = shape.inputs(type = "shadingEngine", c = 1, p = 1)
                    isattr = inAttrLst[0][1]
                    idattr = inAttrLst[0][0]
                    isattr // idattr
                    groupID = [g for g in historyLst if g.type() == "groupId"]
                    pm.delete(groupID)
    
    pm.confirmDialog( title=u'提示', message=u'groupId清理完成', button=['OK'], defaultButton='OK')
    
if __name__ == "__main__":
    delGroupId()