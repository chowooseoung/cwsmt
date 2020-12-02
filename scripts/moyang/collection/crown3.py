#-*- coding:utf-8 -*-

import pymel.core as pm


def create_controller():
	curves = list()
	curves.append(pm.curve(p=[(11.60449796597434, -0.03464998433728117, 2.2090302105806376), (11.604497965974343, -0.03464998433726957, -2.2595581907035185), (11.60449796597434, -0.03464998433726785, -2.9634415627964925), (11.416693407109411, 0.4514234796436653, -3.4366366007094857), (11.95738435318334, 0.8802254634574828, -3.6060886916170887), (13.057904708926879, 3.0355212386073243, -5.548893272131497), (12.9326524307119, 3.988744359884869, -5.515331904402336), (12.73015170498821, 4.207690728659596, -5.696884400996103), (12.555577241566096, 4.207690728659596, -5.999256623469279), (11.473297274382862, 4.207690728659592, -7.873820495747069), (11.29872250379523, 4.207690728659596, -8.176192718220262), (11.242743734154839, 3.98874435988487, -8.442339679812228), (11.334434798223413, 3.0355212386073243, -8.534030743880798), (9.013056850280663, 1.104271859788768, -8.505037717496997), (8.66405997962756, 0.44429293718889695, -8.183845417040304), (8.348162938887599, -0.04178059322617711, -8.583087022090641), (7.738582311283553, -0.041780593226177776, -8.935028575268767), (3.868669239009117, -0.041780593226180385, -11.169322775910473), (3.25908861140507, -0.041780593226182494, -11.521264329088607), (2.7553875432733634, 0.4442929039718183, -11.595218824897591), (2.8551869350762633, 1.1042718597887626, -12.060284866950244), (1.7234684478310056, 3.035521238607412, -14.08292416116784), (1.689907233684634, 3.988744359884854, -13.957671882953049), (1.431427891903478, 4.20769072865956, -13.87307726437211), (1.0822785811025963, 4.207690728659554, -13.87307726437211), (-1.0822827355072075, 4.20769072865956, -13.873076650041037), (-1.431432046308095, 4.207690728659565, -13.873076650041035), (-1.6899113880892487, 3.988744359884854, -13.95767126862196), (-1.723472755818386, 3.0355212386074135, -14.08292354683676), (-2.8603414998832717, 1.1042717239609798, -12.060283794850587), (-2.7553916140778933, 0.4442928758768733, -11.595217816586743), (-3.2590926822094937, -0.04178058810405122, -11.52126332077783), (-3.868673309813369, -0.04178058810405061, -11.169321767599799), (-7.738581598827935, -0.04178058810404839, -8.935028629905126), (-8.34816275790501, -0.04178058810404911, -8.583087076727102), (-8.664058735698449, 0.44429284265979896, -8.18384547167683), (-9.018206046675795, 1.104271723960982, -8.505037775589969), (-11.33443432953063, 3.0355212386082355, -8.534030837194335), (-11.24274326546137, 3.9887443598846914, -8.442339773125486), (-11.298722035101244, 4.207690728659231, -8.176192811534268), (-11.473296805688275, 4.207690728659229, -7.873820589062191), (-12.555577080033126, 4.207690728659228, -5.999256870373875), (-12.730151543454605, 4.2076907286592276, -5.696884647901787), (-12.932652269177902, 3.9887443598846763, -5.51533215130884), (-13.057904547393445, 3.0355212386082324, -5.548893519038464), (-11.875969998273087, 1.104271725322532, -3.5552477756199106), (-11.419448462916229, 0.44429291037448215, -3.4113737310311154), (-11.607253021781162, -0.041780586823523425, -2.9381784273815197), (-11.607253021781162, -0.04178058682352359, -2.2342953210251557), (-11.607253021781164, -0.041780586823523314, 2.234291751575974), (-11.607253021781162, -0.04178058682352376, 2.938174857932344), (-11.419448462916229, 0.4442928439403322, 3.411369895845336), (-11.87596999827309, 1.1042715840485817, 3.555243980356575), (-13.057904975086407, 3.0355212386084514, 5.548891062346229), (-12.93265269687116, 3.9887443598846435, 5.5153298481994995), (-12.730151971148015, 4.207690728659146, 5.696882344792265), (-12.555577507726687, 4.207690728659144, 5.999254567264096), (-11.473295697555056, 4.20769072865914, 7.873821050440699), (-11.298720926968187, 4.20769072865914, 8.176192965746983), (-11.242742157328365, 3.98874435988464, 8.442339927337969), (-11.334433221397365, 3.0355212386084434, 8.534030991406638), (-9.018205141593652, 1.104271723053253, 8.505039861695197), (-8.664057884467734, 0.4442928750231797, 8.183847433660917), (-8.348160843727722, -0.04178058895772041, 8.58308903871123), (-7.738580747596845, -0.0417805889577203, 8.93503059188938), (-3.868670864161346, -0.041780588957718634, 11.169322666638433), (-3.259090236557259, -0.04178058895771919, 11.521264219816572), (-2.755388902688946, 0.4442929082402591, 11.595218715625622), (-2.8603386169636886, 1.1042717230532522, 12.060284750765433), (-1.7234701371034853, 3.03552123860735, 14.082923436664187), (-1.6899089229570898, 3.988744359884869, 13.957671158449205), (-1.4314295811757658, 4.207690728659582, 13.873076539868228), (-1.0822801935832729, 4.207690728659582, 13.87307653986823), (1.0822805086968748, 4.207690728659583, 13.87307653986823), (1.4314298962893695, 4.207690728659585, 13.873076539868231), (1.6899092380706962, 3.9887443598848673, 13.957671158449205), (1.7234704522170885, 3.035521238607351, 14.082923436664187), (2.8551882461547677, 1.1042718597885859, 12.060284866950019), (2.755389042080585, 0.4442929371888761, 11.59521882489721), (3.2590903759487233, -0.04178059322608835, 11.52126432908815), (3.868671269289226, -0.04178059322608818, 11.169322775910095), (7.738582747143169, -0.041780593226086016, 8.935028575268918), (8.348162843273869, -0.04178059322608507, 8.583087022090876), (8.664059884013822, 0.444292903971804, 8.183845417040732), (9.01305674861824, 1.1042718597885877, 8.505037717497624), (11.334434798226432, 3.035521238608172, 8.534030517055081), (11.242743734157576, 3.988744359884702, 8.44233945298646), (11.298722503797515, 4.2076907286592595, 8.17619249139521), (11.4732972743846, 4.207690728659255, 7.873820268923045), (12.555577241564269, 4.2076907286592595, 5.999255628737514), (12.730151704985776, 4.2076907286592595, 5.696883406265345), (12.93265243070905, 3.9887443598847048, 5.515330909672299), (13.057904708924216, 3.0355212386081774, 5.54889212381892), (11.867890130260976, 1.1118534313489592, 3.528384317660372), (11.4166934071094, 0.4514234796436462, 3.386108620586614), (11.60449796597434, -0.034649984337281, 2.912913582673614), (11.60449796597434, -0.03464998433728117, 2.2090302105806376), (11.60449796597434, -0.03464998433728117, 2.2090302105806376), (11.604497965974343, -0.03464998433726957, -2.2595581907035185), (11.60449796597434, -0.03464998433726785, -2.9634415627964925)], d=3, per=2, k=[-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0]))
	pm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)
	empty_grp = pm.group(name='crown3', empty=True)
	shapes = [ y for x in curves for y in x.getShapes() ]
	pm.parent(shapes, empty_grp, relative=True, shape=True)
	pm.delete(curves)
	shapes = empty_grp.getShapes()
	for index, shape in enumerate(shapes):
		if index == 0: index = str()
		shape.rename('{0}Shape{1}'.format(empty_grp.name(), index))
	return empty_grp