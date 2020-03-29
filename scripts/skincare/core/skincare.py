#-*- coding:utf=8 -*-

import maya.cmds as mc


def get_skin_node(geo):
    '''
    return skin node
    parameter : geo
    return : skinnode
    '''
    skin = []
    if not mc.objExists(geo):
        return
    hist = mc.listHistory(geo, pdo=1, il=2)
    if hist:
        for i in hist:
            if mc.nodeType(i) == "skinCluster":
                skin.append(i)
        if len(skin) == 0:
            return
        return skin[0]

def get_jnt_list(geo, removenamespace=0):
    '''
    return joint list
    parameter : geo, removenamespace
    return : skin joint
    '''
    skinJoint = None
    skinNode = get_skin_node(geo)
    if skinNode:
        skinJoint = mc.skinCluster(skinNode, q=1, influence=1)
    if not skinJoint:
        return
    if removenamespace == 1:
        for i in range(len(skinJoint)):
            skinJoint[i] = skinJoint[i].replace("{0}:".format(skinJoint[i].split(":")[0]), "")
    return skinJoint

def move_joint(objName):
    '''
    move joint 
    parameter : objName
    '''
    selection = mc.ls(sl=1)
    for i in objName:
        if mc.ls(objName, rn=1):
            return
        skinNode = get_skin_node(i)
        mc.setAttr("{0}.envelope".format(skinNode), 0)
        dup = mc.duplicate(i)
        jointList = get_jnt_list(i)
        dsSkinNode = mc.skinCluster(jointList, dup, tsb=1)
        mc.copySkinWeights(ss=skinNode, ds=dsSkinNode[0], noMirror=1
        , sa="closestPoint", ia=["label", "oneToOne", "oneToOne"])
        mc.skinCluster(skinNode, e=1, ub=1)
        skinNode = mc.skinCluster(jointList, i, tsb=1)
        mc.copySkinWeights(ss=dsSkinNode[0], ds=skinNode[0], noMirror=1
        , sa="closestPoint", ia=["label", "oneToOne", "oneToOne"])
        mc.delete(dup)
        mc.rename(skinNode, "{0}_SC".format(i))
    mc.select(selection)

def o_n_copy(orig, new, ref=0):
    '''
    1:N copy
    parameter : orig, new, ref
    '''
    selection = mc.ls(sl=1) 
    if (len(orig) != 1) or (len(new) == 0):
        return
    if ref == 0:
        origJointList = get_jnt_list(orig[0])   
    elif ref == 1:
        origJointList = get_jnt_list(orig[0], removenamespace=1)
    check = False
    for i in origJointList:
        if not mc.objExists(i):
            print "{0} does not exists".format(i)
            check = True
    if check == True:
        mc.warning("check joint")
        return False
    origSkinNode = get_skin_node(orig[0])
    mc.setAttr("{0}.envelope".format(origSkinNode), 0)
    for i in new:
        skinNode = get_skin_node(i)
        # new object에 바인드가 되있으면 언바인드
        if skinNode:
            mc.skinCluster(skinNode, e=1, ub=1)
        dsName = mc.skinCluster(origJointList, i, tsb=1)[0]
        ssName = get_skin_node(orig[0])
        mc.copySkinWeights(ss=ssName, ds=dsName, noMirror=1
        , sa="closestPoint", ia=["label", "oneToOne", "oneToOne"])
        mc.rename(dsName, "{0}_SC".format(i))
    mc.setAttr("{0}.envelope".format(origSkinNode), 1)
    mc.select(selection)
    print "DONE"

def n_o_copy(orig, new, ref=0):
    '''
    N:1 copy
    parameter : orig, new, ref
    '''
    selection = mc.ls(sl=1)
    if (len(orig) == 0) or (len(new) == 0):
        return
    jointAllList = []
    for i in orig:
        if ref == 0:
            jointList = get_jnt_list(i)   
        elif ref == 1:
            jointList = get_jnt_list(i, removenamespace=1)
        if jointList:
            jointAllList.extend(jointList)
    check = False
    for i in jointAllList:
        if not mc.objExists(i):
            print "{0} does not exists".format(i)
            check = True
    if check == True:
        mc.warning("check joint")
        return False
    if jointAllList:
        jointAllList = [i for i in set(jointAllList)]
        skinNode = get_skin_node(new[0])
        if skinNode:
            mc.skinCluster(skinNode, e=1, ub=1)
        skinNode = mc.skinCluster(jointAllList, new[0], tsb=1)[0]
        mc.select(orig)
        mc.select(new, add=1)
        mc.copySkinWeights(noMirror=1
        , sa="closestPoint", ia=["label", "oneToOne", "oneToOne"])
        mc.rename(skinNode, "{0}_SC".format(new[0]))
    mc.select(selection)
    print "DONE"

def n_n_copy(orig, new, ref=0):
    '''
    N:N copy
    parameter : orig, new, ref
    '''
    selection = mc.ls(sl=1)
    if (len(orig) == 0) or (len(new) == 0):
        return
    if len(orig) != len(new):
        return
    for i in range(len(new)):
        if ref == 0:
            jointList = get_jnt_list(orig[i])   
        elif ref == 1:
            jointList = get_jnt_list(orig[i], removenamespace=1)
        check = False
        for x in jointList:
            if not mc.objExists(x):
                print "{0} does not exists".format(x)
                check = True
        if check == True:
            mc.warning("check joint")
            return False
        origSkinNode = get_skin_node(orig[i])
        mc.setAttr("{0}.envelope".format(origSkinNode), 0)
        skinNode = get_skin_node(new[i])
        if skinNode:
            mc.skinCluster(skinNode, e=1, ub=1)
        dsName = mc.skinCluster(jointList, new[i], tsb=1)[0]
        ssName = get_skin_node(orig[i])
        mc.copySkinWeights(ss=ssName, ds=dsName, noMirror=1
        , sa="closestPoint", ia=["oneToOne", "oneToOne", "oneToOne"])
        mc.rename(dsName, "{0}_SC".format(new[i]))
    mc.setAttr("{0}.envelope".format(origSkinNode), 1)
    mc.select(selection)
    print "DONE"

def export_skin():
    '''
    export skin weight
    '''
    pass

def import_skin():
    '''
    import skin weight
    '''
    pass

