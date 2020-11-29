#-*- coding:utf-8 -*-

import pymel.core as pm


def create_controller():
	curves = list()
	curves.append(pm.curve(p=[(8.422649383544922, 0.0, -1.0000015497207642), (5.0773491859436035, 0.0, -6.794229507446289), (4.7113237380981445, 0.0, -7.42820405960083), (4.077348709106445, 0.0, -7.794229507446289), (3.3452980518341064, 0.0, -7.794229030609131), (-3.3453006744384766, 0.0, -7.7942280769348145), (-4.077351093292236, 0.0, -7.794227600097656), (-4.711325645446777, 0.0, -7.428202152252197), (-5.077351093292236, 0.0, -6.794227600097656), (-8.422649383544922, 0.0, -0.9999995231628418), (-8.788675308227539, 0.0, -0.3660249412059784), (-8.788675308227539, 0.0, 0.3660258650779724), (-8.422649383544922, 0.0, 1.0000004768371582), (-5.077349662780762, 0.0, 6.794229030609131), (-4.711324214935303, 0.0, 7.428203582763672), (-4.077349662780762, 0.0, 7.794229030609131), (-3.345299005508423, 0.0, 7.794229030609131), (3.3453004360198975, 0.0, 7.7942280769348145), (4.077351093292236, 0.0, 7.7942280769348145), (4.711325645446777, 0.0, 7.4282026290893555), (5.077351093292236, 0.0, 6.7942280769348145), (8.422650337219238, 0.0, 0.9999984502792358), (8.788675308227539, 0.0, 0.3660237789154053), (8.788675308227539, 0.0, -0.3660270571708679), (8.422649383544922, 0.0, -1.0000015497207642)], d=1, per=0, k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0]))
	pm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)
	empty_grp = pm.group(name='hexagon0', empty=True)
	shapes = [ y for x in curves for y in x.getShapes() ]
	pm.parent(shapes, empty_grp, relative=True, shape=True)
	pm.delete(curves)
	shapes = empty_grp.getShapes()
	for index, shape in enumerate(shapes):
		if index == 0: index = str()
		shape.rename('{0}Shape{1}'.format(empty_grp.name(), index))
	return empty_grp