#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(0.0, 0.4432776750217552, 0.0), (0.44327767502175525, 1.329833025065266, 0.0), (1.1081941875543881, 1.329833025065266, 0.0), (0.0, -0.8865553500435104, 0.0), (-1.1081941875543881, 1.329833025065266, 0.0), (-0.44327767502175525, 1.329833025065266, 0.0), (0.0, 0.4432776750217552, 0.0)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
	em = mc.group(n='v', em=1)
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
