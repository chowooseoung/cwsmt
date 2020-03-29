#-*- coding:utf-8 -*-

import maya.cmds as mc
import maya.mel as mel


def shape_list(select, removeorig=0, type=0):
    shapeList = []
    for i in range(len(select)):
        shapeList.append([])
        shapeList[i].extend(mc.listRelatives(select[i], s=1))
    removeList =[]
    for i in range(len(shapeList)):
        removeList.append([])
        for x in range(len(shapeList[i])):
            if shapeList[i][x].endswith("Orig"):
                removeList[i].append(shapeList[i][x])
    
    for i in range(len(removeList)):
        for x in range(len(removeList[i])):
            shapeList[i].remove(removeList[i][x])
            if removeorig == 1:
                print "delete {0}".format(removelist[i][x])
                mel.eval("DeleteHistory;")
                mc.delete(shapeList[i][0], ch=1)
        
    if type == 1:
        for i in range(len(shapeList)):
            for x in range(len(shapeList[i])):
                shapeList[i][x] = mc.nodeType(shapeList[i][x])
        return shapeList
    elif type == 0:
        return shapeList