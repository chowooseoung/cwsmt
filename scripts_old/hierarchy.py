#-*- coding:utf-8 -*-

import maya.cmds as mc
import pprint


def hierarchy_list():
    '''
    maya transform hierarchy key, value dict return

    return
    '''
    selection = []
    selection.append(mc.ls(sl=1))
    # 모든 차일드 풀패스 
    fullPath = mc.listRelatives(selection[0], ad=1, f=1, type='transform')
    if fullPath == None:
        mc.warning("this obj don't have child")
        return
    countList = []
    for i in fullPath:
        temp = i.count("|")
        countList.append(temp)
    countList.sort()
    keyList = []
    keyValueDict = {}
    for i in range(countList[-1]-1):
        selection.append([])
        for x in selection[i]:
            childList = mc.listRelatives(x, c=1, type='transform')
            if type(childList) != type(None):
                selection[i+1].extend(childList)
                keyList.append(x)
                keyValueDict[x] = childList
    print "keyList :"
    pprint.pprint(keyList)
    print "keyValueDict :"
    pprint.pprint(keyValueDict)
    return keyList, keyValueDict

def re_hierarchy(key, keyValue):
    for i in range(len(key)):
        parent = key[i]
        child = keyValue[key[i]]
        mc.parent(child, parent)

    