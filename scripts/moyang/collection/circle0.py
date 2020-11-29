#-*- coding:utf-8 -*-

import pymel.core as pm


def create_controller():
	curves = list()
	curves.append(pm.curve(p=[(6.268892999129796, 3.8385898727907785e-16, -6.268892999129797), (5.42858585848873e-16, 5.42858585848873e-16, -8.865553500435102), (-6.268892999129796, 3.8385898727907775e-16, -6.268892999129795), (-8.865553500435105, 2.814188495204822e-32, -4.595918590019864e-16), (-6.268892999129796, -3.838589872790778e-16, 6.268892999129796), (-8.88068557568258e-16, -5.428585858488734e-16, 8.865553500435107), (6.268892999129796, -3.8385898727907775e-16, 6.268892999129795), (8.865553500435105, -7.402943368088079e-32, 1.2089924006239672e-15), (6.268892999129796, 3.8385898727907785e-16, -6.268892999129797), (5.42858585848873e-16, 5.42858585848873e-16, -8.865553500435102), (-6.268892999129796, 3.8385898727907775e-16, -6.268892999129795)], d=3, per=2, k=[-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]))
	pm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)
	empty_grp = pm.group(name='circle0', empty=True)
	shapes = [ y for x in curves for y in x.getShapes() ]
	pm.parent(shapes, empty_grp, relative=True, shape=True)
	pm.delete(curves)
	shapes = empty_grp.getShapes()
	for index, shape in enumerate(shapes):
		if index == 0: index = str()
		shape.rename('{0}Shape{1}'.format(empty_grp.name(), index))
	return empty_grp