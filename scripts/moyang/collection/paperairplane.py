#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(-4.982654, 0.0, 0.0), (4.946539, 0.0, -3.309731), (4.946539, 0.0, 3.309731), (-4.982654, 0.0, 0.0), (4.946539, 3.309731, 0.0), (4.946539, -3.309731, 0.0), (-4.982654, 0.0, 0.0)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
	em = mc.group(n='paperairplane', em=1)
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
