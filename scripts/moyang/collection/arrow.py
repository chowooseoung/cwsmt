#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(-4.962619, 0.0, 0.0), (-2.229371, 0.0, -1.366624), (-2.8545, 0.0, -0.140467), (3.237123, 0.0, -0.144552), (3.992161, 0.0, -1.009235), (4.925689, 0.0, -1.009235), (4.019556, 0.0, 0.0), (4.925689, 0.0, 1.009235), (3.992161, 0.0, 1.009235), (3.237123, 0.0, 0.130692), (-2.8545, 0.0, 0.130692), (-2.229371, 0.0, 1.366624), (-4.962619, 0.0, 0.0)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]))
	em = mc.group(n='arrow', em=1)
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
