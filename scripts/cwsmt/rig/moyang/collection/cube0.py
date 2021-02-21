#-*- coding:utf-8 -*-

import pymel.core as pm


def create_controller():
	curves = list()
	curves.append(pm.curve(p=[(-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0]))
	pm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)
	empty_grp = pm.group(name='cube0', empty=True)
	shapes = [ y for x in curves for y in x.getShapes() ]
	pm.parent(shapes, empty_grp, relative=True, shape=True)
	pm.delete(curves)
	shapes = empty_grp.getShapes()
	for index, shape in enumerate(shapes):
		if index == 0: index = str()
		shape.rename('{0}Shape{1}'.format(empty_grp.name(), index))
	return empty_grp