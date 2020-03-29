#-*- coding:utf-8 -*-

import maya.cmds as mc


def scale_value(origobject, resultobject, multiplyvalue=1, shape=0):
    if shape == 1:
        origObjectBoundBox = mc.getAttr(mc.listRelatives(origobject, s=1)[0] + ".boundingBoxSize")[0]
    elif shape == 0:
        origObjectBoundBox = mc.getAttr(origobject + ".boundingBoxSize")[0]
    
    resultObjectBoungBox = mc.getAttr(resultobject + ".boundingBoxSize")[0]

    origObjectValueMax = max(origObjectBoundBox)
    resultObjectValueMax = max(resultObjectBoungBox)

    resultObjectOldScale = mc.xform(resultobject, q=1, s=1, r=1)
    boundDifferenceValue = origObjectValueMax / resultObjectValueMax
    scaleValue = [resultObjectOldScale[0] * boundDifferenceValue * multiplyvalue,
                    resultObjectOldScale[1] * boundDifferenceValue * multiplyvalue,
                    resultObjectOldScale[2] * boundDifferenceValue * multiplyvalue,]

    return scaleValue