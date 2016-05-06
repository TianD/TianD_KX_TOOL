#coding:utf-8
'''
Created on 2016年5月5日 下午4:11:48

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:

'''
import pymel.core as pm
import utils.name as name

def createObjectSet(setName, objLst = [], exclusiveness = False, partition = None, increment = False):
    '''
    create an objectSet.
    @param    setName           string         :    This objectSet's name.
    @param    objLst            list           :    Objects which belongs this objectSet.
    @param    exclusiveness     bool           :    Whether is this objectSet mutually exclusive with another objectSet in one partition.
    @param    partition         node or string :    When exclusiveness flag is True, partitin should be assigned a partition node. Ignore when exclusiveness flag is False.
    @param    increment         bool           :    Whether to use the existed one or create an increment one When the named objectSet has been existed.
                                                    If the existed objectSet will be used, ignore exclusiveness flag and partition flag.
    @result                     node 
    '''
    useExisted = False
    if not pm.objExists(setName):
        objSet = pm.sets(em=1, name = setName)
    elif pm.objExists(setName) and increment :
        setName = name.compileNodeName(setName)
        objSet = pm.sets(em=1, name = setName)
    else:
        objSet = pm.PyNode(setName)
        useExisted = True
        
    if not useExisted and exclusiveness :
        partition.addMember(objSet)
    
    if objLst:
        #objSet.addMembers(objLst)
        pm.sets(objSet, e=1, forceElement = objLst)
    
    return objSet
    
def createPartition(partitionName, sets = [], increment = False):
    '''
    create a partition.
    @param    partitionName    string          :    This partition's name.
    @param    sets             list            :    Sets which belongs this partition.
    @param    increment        bool            :    Whetch to use the existed one or create an increment one When the named partition has been existed.
    @result                    node
    '''
    if not pm.objExists(partitionName):
        partition = pm.createNode("partition", name = partitionName)
    elif pm.objExists(partitionName) and increment :
        partitionName = name.compileNodeName(partitionName)
        partition = pm.createNode("partition", name = partitionName)
    else :
        partition = pm.PyNode(partitionName)
        
    if sets:
        partition.addMember(sets)

        
    return partition

    