#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(0.0, 0.0, 0.5773502588272094), (-0.4999999999999999, 0.0, -0.2886751294136046), (0.4999999999999999, 0.0, -0.2886751294136046), (0.0, 0.0, 0.5773502588272094)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0]))
	em = mc.group(n='semo', em=1)
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
