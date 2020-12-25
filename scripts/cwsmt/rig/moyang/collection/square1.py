#-*- coding:utf-8 -*-

import pymel.core as pm


def create_controller():
	curves = list()
	curves.append(pm.curve(p=[(-7.43918130058371, 0.0, 7.43918130058371), (7.43918130058371, 0.0, 7.43918130058371), (7.43918130058371, 0.0, -7.43918130058371), (-7.43918130058371, 0.0, -7.43918130058371), (-7.43918130058371, 0.0, 7.43918130058371)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0]))
	pm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)
	empty_grp = pm.group(name='square1', empty=True)
	shapes = [ y for x in curves for y in x.getShapes() ]
	pm.parent(shapes, empty_grp, relative=True, shape=True)
	pm.delete(curves)
	shapes = empty_grp.getShapes()
	for index, shape in enumerate(shapes):
		if index == 0: index = str()
		shape.rename('{0}Shape{1}'.format(empty_grp.name(), index))
	return empty_grp