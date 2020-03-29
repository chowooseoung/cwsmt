#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(5.0, 0.0, 5.0), (-5.0, 0.0, 5.0), (-5.0, 0.0, -5.0), (5.0, 0.0, -5.0), (5.0, 0.0, 5.0), (0.0, 10.0, 0.0), (-5.0, 0.0, 5.0), (-5.0, 0.0, -5.0), (0.0, 10.0, 0.0), (5.0, 0.0, -5.0), (5.0, 0.0, 5.0), (0.0, 10.0, 0.0), (-5.0, 0.0, 5.0)], d=1, per=0, k=[0.0, 4.0, 8.0, 12.0, 16.0, 24.485281, 32.970563, 36.970563, 45.455844, 53.941125, 57.941125, 66.426407, 74.911688]))
	em = mc.group(n='pyramid', em=1)
	mc.select(crvList)
	for curve in crvList:
		mc.makeIdentity(curve, a=1, t=1, r=1, s=1, n=0, pn=1)
		mc.xform(curve, ws=1, piv=(0,0,0))
		shapeNode = mc.listRelatives(curve, s=1)
		shapeNode = mc.rename(shapeNode, '{0}Shape'.format(em))
		mc.parent(shapeNode, em, r=1, s=1)
		mc.delete(curve)
	mc.select(em)
	return em
