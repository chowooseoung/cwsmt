#-*- coding:utf-8 -*-

import maya.cmds as mc


def ikfk_match(fkjoint=[], ikjoint=[], fkcon=[], ikcon=[], selection=[], bake=1):
    '''
    fk = [fkjoint1, fkjoint2, fkjoint3]
    ik = [ikjoint1, ikjoint2, ikjoint3]
    selection = select controller list
    bake = key bake True/False
    '''
    selection = mc.ls(sl=1)

    if len(selection) != 1:
        return

    namespace = mc.ls(sl=1, sns=1)[1]
    
    if not namespace == ":":
        for i in range(len(fkjoint)):
            fkjoint[i] = "{0}:{1}".format(namespace, fkjoint[i])
        for i in range(len(ikjoint)):
            ikjoint[i] = "{0}:{1}".format(namespace, ikjoint[i])
        for i in range(len(fkcon)):
            fkcon[i] = "{0}:{1}".format(namespace, fkcon[i])
        for i in range(len(ikcon)):
            ikcon[i] = "{0}:{1}".format(namespace, ikcon[i])
    
    currentIkFk = selection.split("_")[-2]
    if currentIkFk == "ik":
        source = ikjoint
        target = fkcon
    elif currentIkFk == "fk":
        source = fkjoint
        target = ikcon

    if bake == 0:
        for i in range(len(source)):
            mc.xform(target[i], t=mc.xform(source[i], q=1, t=1, ws=1), ws=1)
            mc.xform(target[i], ro=mc.xform(source[i], q=1, ro=1, ws=1), ws=1)
            return

    if mc.keyframe(selection, q=1) == None:
        return
    keylen = list(set(mc.keyframe(selection, q=1)))
    keylen.sort()

    startFrame = keylen[0]
    endFrame = keylen[-1]+1
    ct = mc.currentTime(q=1)

    for i in range(1, int(endFrame-startFrame)+1):
        mc.currentTime(i)
        for x in range(len(source)):
            mc.xform(target[x], t=mc.xform(source[x], q=1, t=1, ws=1), ws=1)
            mc.xform(target[x], ro=mc.xform(source[x], q=1, ro=1, ws=1), ws=1)
            
            mc.setKeyframe(target[x], 
                            at=["tx", "ty", "tz", "rx", "ry", "rz"], 
                            breakdown=0, 
                            controlPoints=0, 
                            shape=0)
    mc.currentTime(ct)