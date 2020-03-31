#-*- coding:utf-8 -*-

import maya.cmds as mc
import maya.mel as mel

import shapelist as sl
import scalevalue as sc
reload(sl)
reload(sc)

def replace_con(newcon):
    repCurve = list(newcon)

    selection = mc.ls(sl=1)
    selShapeList = sl.shape_list(selection, removeorig=0)
    selShapeTypeList = sl.shape_list(selection, removeorig=0, type=1)
    crvShapeList = sl.shape_list(repCurve, removeorig=0)

    shapeColor = []
    for i in range(len(selShapeTypeList)):
        if mc.getAttr("{0}.overrideEnabled".format(selShapeList[i][0])):
            if mc.getAttr("{0}.overrideRGBColors".format(selShapeList[i][0])):
                shapeColor.append(mc.getAttr("{0}.overrideColorRGB".format(selShapeList[i][0]))[0])
            elif not mc.getAttr("{0}.overrideRGBColors".format(selShapeList[i][0])):
                shapeColor.append(mc.getAttr("{0}.overrideColor".format(selShapeList[i][0])))
        elif not mc.getAttr("{0}.overrideEnabled".format(selShapeList[i][0])):
            shapeColor.append([])

    dupList = []
    for i in range(len(selection)):
        dupList.append([])
        for x in range(len(crvShapeList[0])):
            dupList[i].extend(mc.duplicateCurve(crvShapeList[0][x], ch=0))
    
    tempGrp = []
    for i in range(len(dupList)):
        tempGrp.append(mc.group(n="temp#", em=1))
        for x in range(len(dupList[i])):
            mc.pickWalk(dupList[i][x], d="down")
            mc.select(tempGrp[i], add=1)
            mc.parent(r=1, s=1)
            mc.delete(dupList[i][x])
    crv = []
    for i in range(len(selection)):
        dup = []
        for x in range(len(selShapeList[i])):
            dup.append(mc.duplicateCurve(selShapeList[i][x], ch=0)[0])
        crv = combine_curve_shape(dup)
        scaleValue = sc.scale_value(crv, tempGrp[i])
        mc.xform(tempGrp[i], s=scaleValue, ws=1)
        mc.makeIdentity(tempGrp[i], a=1, t=0, r=0, s=1, n=0, pn=1)
        mc.delete(crv)

    for i in selShapeList:
        mc.delete(i)

    tempShapeList = sl.shape_list(tempGrp, removeorig=0)

    for i in range(len(tempShapeList)):
        for x in range(len(tempShapeList[i])):
            mc.parent(tempShapeList[i][x], selection[i], r=1, s=1)
    for i in tempGrp:
        mc.delete(i)

    selShapeList = sl.shape_list(selection, removeorig=0)

    for i in range(len(selShapeList)):
        number = 0
        for x in range(len(selShapeList[i])):
            if number == 0:
                replaceName = "{0}Shape".format(selection[i])
            elif number > 0:
                replaceName = "{0}Shape{1}".format(selection[i], number)
            mc.rename(selShapeList[i][x], replaceName)
            number += 1

    selShapeList = sl.shape_list(selection, removeorig=0)
    selShapeTypeList = sl.shape_list(selection, removeorig=0, type=1)
    for i in range(len(selShapeList)):
        for x in range(len(selShapeList[i])):
            if type(shapeColor[i]) == type(1):
                mc.setAttr("{0}.overrideEnabled".format(selShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideRGBColors".format(selShapeList[i][x]), 0)
                mc.setAttr("{0}.overrideColor".format(selShapeList[i][x]), shapeColor[i])
            elif type(shapeColor[i]) == type([]):
                pass
            elif type(shapeColor[i]) == type(()):
                mc.setAttr("{0}.overrideEnabled".format(selShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideRGBColors".format(selShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideColorRGB".format(selShapeList[i][x]), shapeColor[i][0],
                           shapeColor[i][1], shapeColor[i][2])
    mc.select(selection)

def mirror_con(scale=(-1, 1, 1), left="L", right="R"):
    selection = mc.ls(sl=1)
    targetSelection = []
    for i in selection:
        if i.startswith(left):
            targetSelection.append(i.replace(left, right))
        if i.startswith(right):
            targetSelection.append(i.replace(right, left))

    shapeList = sl.shape_list(selection, removeorig=0)
    shapeTypeList = sl.shape_list(selection, removeorig=0, type=1)
    targetShapeList = sl.shape_list(targetSelection, removeorig=0)
    targetShapeTypeList = sl.shape_list(targetSelection, removeorig=0, type=1)
    shapeColor = []

    for i in range(len(targetShapeTypeList)): # color 가져오기
        if mc.getAttr("{0}.overrideEnabled".format(targetShapeList[i][0])):
            if mc.getAttr("{0}.overrideRGBColors".format(targetShapeList[i][0])):
                shapeColor.append(mc.getAttr("{0}.overrideColorRGB".format(targetShapeList[i][0]))[0])
            elif not mc.getAttr("{0}.overrideRGBColors".format(targetShapeList[i][0])):
                shapeColor.append(mc.getAttr("{0}.overrideColor".format(targetShapeList[i][0])))
        elif not mc.getAttr("{0}.overrideEnabled".format(targetShapeList[i][0])):
            shapeColor.append([])

    for i in targetShapeList:
        mc.delete(i)

    dupList = [] # 컨트롤러 카피 
    for i in range(len(shapeTypeList)):
        number = 0
        dupList.append([])
        for x in range(len(shapeTypeList[i])):
            
            dupList[i].extend(mc.duplicateCurve(shapeList[i][x], ch=0))
            mc.xform(dupList[i][x], ro=mc.xform(selection[i], q=1, ro=1, ws=1), ws=1)
            mc.parent(dupList[i][x], targetSelection[i])
            mc.setAttr("{0}.t".format(dupList[i][x]), 0,0,0)
            mc.select(d=1)
            mc.select("{0}.cv[:]".format(dupList[i][x]))
            
            mc.scale(scale[0], scale[1], scale[2], ws=1)
            # if scale[0]*scale[1]*scale[2]<0:
            #     mc.reverseCurve(dupList[i][x], ch=0)
            mc.select(d=1)
            mc.makeIdentity(dupList[i][x], a=1, t=0, r=1, s=1, n=0, pn=1)
            
            mc.delete(dupList[i][x], ch=1)
            
            shapeNode = mc.pickWalk(dupList[i][x], d="down")
            mc.select(shapeNode)
            mc.select(targetSelection[i], add=1)
            mc.parent(r=1, s=1)
            mc.delete(dupList[i][x])

            if number == 0:
                replaceName = "{0}Shape".format(selection[i])
            elif number > 0:
                replaceName = "{0}Shape{1}".format(selection[i], number)
            mc.rename(shapeList[i][x], replaceName)
            number += 1

    targetShapeList = sl.shape_list(targetSelection, removeorig=0) # 이름 수정
    for i in range(len(targetShapeList)):
        number = 0
        for x in range(len(targetShapeList[i])):
            if number == 0:
                replaceName = "{0}Shape".format(targetSelection[i])
            elif number > 0:
                replaceName = "{0}Shape{1}".format(targetSelection[i], number)
            mc.rename(targetShapeList[i][x], replaceName)
            number += 1

    revReplaceShapeList = sl.shape_list(targetSelection, removeorig=0)

    for i in range(len(revReplaceShapeList)):
        for x in range(len(revReplaceShapeList[i])):
            if type(shapeColor[i]) == type(1):
                mc.setAttr("{0}.overrideEnabled".format(revReplaceShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideRGBColors".format(revReplaceShapeList[i][x]), 0)
                mc.setAttr("{0}.overrideColor".format(revReplaceShapeList[i][x]), shapeColor[i])
            elif type(shapeColor[i]) == type([]):
                pass
            elif type(shapeColor[i]) == type(()):
                mc.setAttr("{0}.overrideEnabled".format(revReplaceShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideRGBColors".format(revReplaceShapeList[i][x]), 1)
                mc.setAttr("{0}.overrideColorRGB".format(revReplaceShapeList[i][x]), shapeColor[i][0], shapeColor[i][1], shapeColor[i][2])
    mc.select(selection)

def combine_curve_shape(crv):
    selection = list(crv)
    mc.makeIdentity(selection, a=1, t=1, r=1, s=1, n=0, pn=1)
    em = mc.group(n="combineCurve", em=1)
    for i in selection:
        mc.xform(i, ws=1, piv=(0, 0, 0))
        shapeNode = mc.listRelatives(i, s=1)
        mc.parent(shapeNode, em, r=1, s=1)
        mc.delete(i)
    mc.select(em)
    return em

def get_shape(crv, name):
    '''
    return curve create method 
    '''
    mc.delete(crv, ch=True)
    shapes = mc.listRelatives(crv, shapes=True)

    tempTxt = ""
    for i in shapes:
        curveDegree = mc.getAttr("{0}.degree".format(i))
        spans = mc.getAttr("{0}.spans".format(i))
        period = mc.getAttr("{0}.f".format(i))
        cv = spans + curveDegree

        infoNode = mc.createNode("curveInfo")
        mc.connectAttr(("{0}.worldSpace[0]".format(i)), ("{0}.inputCurve".format(infoNode)))
        knots = mc.getAttr("{0}.knots".format(infoNode))[0]
        knotsList = []
        for e in knots:
            knotsList.append(e)
        controlVerts = [mc.getAttr("{0}.controlPoints[{1}]".format(i, x))[0] for x in range(cv)]

        if period == 0:
            periodNode = 0
        else:
            periodNode = 1

        tempTxt += "\tcrvList.append(mc.curve(p={0}, d={1}, per={2}, k={3}))\n".format(
        controlVerts, curveDegree, periodNode, knotsList)
        
        mc.delete(infoNode)

    curvePyTxt = "#-*- coding:utf-8 -*-\n\n"
    curvePyTxt += "import maya.cmds as mc\n\n"
    curvePyTxt += "def create():\n"
    curvePyTxt += "\tcrvList = []\n"
    curvePyTxt += "{0}".format(tempTxt)
    curvePyTxt += "\tem = mc.group(n='{0}', em=1)\n".format(name)
    curvePyTxt += "\tmc.select(crvList)\n"
    curvePyTxt += "\tfor curve in crvList:\n"
    curvePyTxt += "\t\tmc.makeIdentity(curve, a=1, t=1, r=1, s=1, n=0, pn=1)\n"
    curvePyTxt += "\t\tmc.xform(curve, ws=1, piv=(0,0,0))\n"
    curvePyTxt += "\t\tshapeNode = mc.listRelatives(curve, s=1)\n"
    curvePyTxt += "\t\tshapeNode = mc.rename(shapeNode, '{0}Shape'.format(em))\n"
    curvePyTxt += "\t\tmc.parent(shapeNode, em, r=1, s=1)\n"
    curvePyTxt += "\t\tmc.delete(curve)\n"
    curvePyTxt += "\tmc.select(em)\n"
    curvePyTxt += "\treturn em\n"

    return curvePyTxt
