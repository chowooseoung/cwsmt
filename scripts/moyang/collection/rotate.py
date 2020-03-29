#-*- coding:utf-8 -*-

import maya.cmds as mc

def create():
	crvList = []
	crvList.append(mc.curve(p=[(0.0, 0.0, -3.5999999999999996), (0.0, 0.0, -4.8), (1.241004, 0.0, -4.6322844), (2.3979936, 0.0, -4.153035), (3.3941388, 0.0, -3.3941406), (4.1530386, 0.0, -2.3979923999999997), (4.632279, 0.0, -1.2410046000000001), (4.800037199999999, 0.0, 3.093192e-07), (4.632279, 0.0, 1.241004), (4.1530386, 0.0, 2.3979936), (3.3941388, 0.0, 3.3941388), (2.3979936, 0.0, 4.1530386), (1.241004, 0.0, 4.632279), (0.0, 0.0, 4.800037199999999), (-1.241004, 0.0, 4.632279), (-2.3979936, 0.0, 4.1530386), (-3.3941388, 0.0, 3.3941388), (-4.1530386, 0.0, 2.3979936), (-4.632279, 0.0, 1.241004), (-4.800037199999999, 0.0, 3.093192e-07), (-6.0704856, 0.0, 0.0), (-4.1755265999999995, 0.0, -3.789918), (-2.2805676, 0.0, 0.0), (-3.6000275999999998, 0.0, 2.3215859999999999e-07), (-3.4742094, 0.0, 0.9307536), (-3.1147788, 0.0, 1.7984946), (-2.5456043999999998, 0.0, 2.5456038), (-1.7984946, 0.0, 3.1147788), (-0.9307536, 0.0, 3.4742094), (0.0, 0.0, 3.6000275999999998), (0.9307536, 0.0, 3.4742094), (1.7984946, 0.0, 3.1147788), (2.5456043999999998, 0.0, 2.5456038), (3.1147788, 0.0, 1.7984946), (3.4742094, 0.0, 0.9307536), (3.6000275999999998, 0.0, 2.3215859999999999e-07), (3.4742094, 0.0, -0.9307542), (3.1147788, 0.0, -1.798494), (2.5456043999999998, 0.0, -2.5456056), (1.7984946, 0.0, -3.1147764), (0.9307536, 0.0, -3.4742129999999998), (0.0, 0.0, -3.5999999999999996)], d=1, per=0, k=[0.0, 2.0, 4.087143, 6.174343, 8.261489, 10.348646, 12.435838, 14.522991, 16.610143, 18.697338, 20.78449, 22.871642, 24.958836, 27.045989, 29.133141, 31.220335, 33.307488, 35.394639, 37.481834, 39.568986, 41.6864, 48.748496, 55.810591, 58.009692, 59.575056, 61.140451, 62.705816, 64.271181, 65.836575, 67.40194, 68.967305, 70.532699, 72.098064, 73.663429, 75.228823, 76.794188, 78.359554, 79.924946, 81.490314, 83.055675, 84.621073, 86.186431]))
	em = mc.group(n='rotate', em=1)
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
