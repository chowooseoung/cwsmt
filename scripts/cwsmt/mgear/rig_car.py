# -*- coding:utf-8 -*-

import pymel.core as pm
import mgear.rigbits as rb


def wheel_rig(index, hostui, drive, ball, ballEnd, wheel, direction):
    """
    index(str) : sideindex  e.x. L0, L1, L2
    direction(bool) : first wheel(True), another wheel(False)
    """
    host_con = pm.PyNode(hostui.replace("root", "ctl"))
    
    host_con.addAttr(index, type="enum", en="_____", keyable=True)
    wheel_radius = abs(wheel.ty.get())
    host_con.addAttr("{0}WheelDrive".format(index), type="float", keyable=True, defaultValue=0)
    host_con.addAttr("{0}WheelRadius".format(index), type="float", keyable=True, defaultValue=0)
    host_con.attr("{0}WheelRadius".format(index)).set(wheel_radius)
    pma = pm.createNode("plusMinusAverage")
    pma.input1D[0].set(pm.PyNode("chasis_C0_root").ty.get()*-1)
    host_con.attr("{0}WheelRadius".format(index)) >> pma.input1D[1]
    pma.output1D >> ball.ty

    if direction:
        steer_radius = abs(ballEnd.tx.get())
        host_con.addAttr("{0}SteerDrive".format(index), type="float", keyable=True, defaultValue=0)
        host_con.addAttr("{0}SteerRadius".format(index), type="float", keyable=True, defaultValue=0)
        host_con.attr("{0}SteerRadius".format(index)).set(steer_radius)
        if index.startswith("L"):
            host_con.attr("{0}SteerRadius".format(index)) >> ballEnd.tx
        else:
            inverse_mul = pm.createNode("multiplyDivide")
            inverse_mul.input1X.set(-1)
            host_con.attr("{0}SteerRadius".format(index)) >> inverse_mul.input2X
            inverse_mul.outputX >> ballEnd.tx

    drive_con = pm.PyNode(drive.replace("root", "ctl"))
    drive_con.addAttr("autoWheel{0}".format(index), type="bool", keyable=True, defaultValue=1)
    drive_con.addAttr("wheelSpin{0}".format(index), type="float", keyable=True, defaultValue=0)
    
    # size
    world_con = pm.PyNode("world_ctl")
    scale_mul = pm.createNode("multiplyDivide")
    host_con.attr("{0}WheelRadius".format(index)) >> scale_mul.input1X
    world_con.size >> scale_mul.input2X
    if direction:
        host_con.attr("{0}SteerRadius".format(index)) >> scale_mul.input1Y
        world_con.size >> scale_mul.input2Y
    
    # wheel t >> ball t
    ball_con = pm.PyNode(ball.replace("root", "ctl"))
    wheel_con = pm.PyNode(wheel.replace("root", "ctl"))
    ball_t = rb.addNPO(ball_con)[0]
    ball_t.rename("{0}_t".format(ball_con.name()))
    wheel_con.t >> ball_t.t
    
    # wheel 
    wheel_pma = pm.createNode("plusMinusAverage")
    drive_con.attr("wheelSpin{0}".format(index)) >> wheel_pma.input1D[0]
    host_con.attr("{0}WheelDrive".format(index)) >> wheel_pma.input1D[1]

    ball_end_con = pm.PyNode(ballEnd.replace("root", "ctl"))
    ball_end_wheel = rb.addNPO(ball_end_con)[0]
    ball_end_wheel.rename("{0}_wheel".format(ball_end_con.name()))

    if direction:
        drive_pma = pm.createNode("plusMinusAverage")

        wheel_pma.output1D >> drive_pma.input1D[0]
        host_con.attr("{0}SteerDrive".format(index)) >> drive_pma.input1D[1]
        
        drive_pma.output1D >> ball_end_wheel.rx
    else:
        wheel_pma.output1D >> ball_end_wheel.rx
    
    # steer
    if direction:
        steer_mul = pm.createNode("multiplyDivide")
        drive_con.steering >> steer_mul.input1X
        steer_mul.input2X.set(360)
        steer_mul.operation.set(2)

        wheel_mul = pm.createNode("multiplyDivide")
        scale_mul.outputX >> wheel_mul.input1X
        wheel_mul.input2X.set(6.283185)

        steer_mul1 = pm.createNode("multiplyDivide")
        scale_mul.outputY >> steer_mul1.input1X
        steer_mul1.input2X.set(6.283185)

        steer_distance_mul = pm.createNode("multiplyDivide")
        steer_mul.outputX >> steer_distance_mul.input1X
        steer_mul1.outputX >> steer_distance_mul.input2X

        steer_drive_mul = pm.createNode("multiplyDivide")
        steer_distance_mul.outputX >> steer_drive_mul.input1X
        wheel_mul.outputX >> steer_drive_mul.input2X
        steer_drive_mul.operation.set(2)

        steer_drive_distance_mul = pm.createNode("multiplyDivide")
        steer_drive_mul.outputX >> steer_drive_distance_mul.input1X
        steer_drive_distance_mul.input2X.set(-360)
        steer_drive_distance_mul.outputX >> host_con.attr("{0}SteerDrive".format(index))
    
    # ref shape
    wheel_cns = pm.PyNode(ballEnd.replace("root", "ik_cns"))

    wheel_ref, wheel_make = pm.circle(name="wheel_{0}_refShape".format(index), normal=(1,0,0))

    pm.parent(wheel_ref, wheel_cns)

    wheel_ref.t.set(0, 0, 0)
    wheel_ref.r.set(0, 0, 0)

    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    ( wheel_ref.attr(attr).lock(True) for attr in attrs )
    ( wheel_ref.attr(attr).setKeyable(False) for attr in attrs )
    wheel_ref.overrideEnabled.set(True)
    wheel_ref.overrideDisplayType.set(True)

    host_con.attr("{0}WheelRadius".format(index)) >> wheel_make.radius

    # steer
    ball_con = pm.PyNode(ball.replace("root", "ctl"))
    ball_steering = rb.addNPO(ball_con)[0]
    ball_steering.rename("{0}_steering".format(ball_con.name()))
    drive_con.steering >> ball_steering.ry

    exp = '''
global vector $vPos{index} = << 0, 0, 0 >>;
int $direction{index} = 1;
vector $vPosChange{index} = `getAttr {drive}.translate`;
float $cx{index} = $vPosChange{index}.x - $vPos{index}.x;
float $cy{index} = $vPosChange{index}.y - $vPos{index}.y;
float $cz{index} = $vPosChange{index}.z - $vPos{index}.z;
float $distance{index} = sqrt( `pow $cx{index} 2` + `pow $cy{index} 2` + `pow $cz{index} 2` );
float $angle{index} = {drive}.rotateY%360;

if ( ( $vPosChange{index}.x == $vPos{index}.x ) && ( $vPosChange{index}.y != $vPos{index}.y ) && ( $vPosChange{index}.z == $vPos{index}.z ) ){{}}
else {{
	if ( $angle{index} == 0 ){{ 
		if ( $vPosChange{index}.z > $vPos{index}.z ) $direction{index} = 1;
		else $direction{index}=-1;}}
	if ( ( $angle{index} > 0 && $angle{index} <= 90 ) || ( $angle{index} <- 180 && $angle{index} >= -270 ) ){{ 
		if ( $vPosChange{index}.x > $vPos{index}.x ) $direction{index} = 1 * $direction{index};
		else $direction{index} = -1 * $direction{index}; }}
	if ( ( $angle{index} > 90 && $angle{index} <= 180 ) || ( $angle{index} < -90 && $angle{index} >= -180 ) ){{
		if ( $vPosChange{index}.z > $vPos{index}.z ) $direction{index} = -1 * $direction{index};
		else $direction{index} = 1 * $direction{index}; }}
	if ( ( $angle{index} > 180 && $angle{index} <= 270 ) || ( $angle{index} < 0 && $angle{index} >= -90 ) ){{
		if ( $vPosChange{index}.x > $vPos{index}.x ) $direction{index} = -1 * $direction{index};
		else $direction{index} = 1 * $direction{index}; }}
	if ( ( $angle{index} > 270 && $angle{index} <= 360 ) || ( $angle{index} < -270 && $angle{index} >= -360 ) ) {{
		if ( $vPosChange{index}.z > $vPos{index}.z ) $direction{index} = 1 * $direction{index};
		else $direction{index} = -1 * $direction{index}; }}
	{ui}.{index}WheelDrive = {ui}.{index}WheelDrive + ( ( $direction{index} * ( ( $distance{index} / ( 6.283185 * {ui}.{index}WheelRadius ) ) * 360.0 ) ) ); }}
$vPos{index} = << {drive}.translateX, {drive}.translateY, {drive}.translateZ >>;
'''.format(drive=drive_con.name(), ui=host_con.name(), index=index)

    pm.expression(name="car_{0}_exp".format(index), string=exp)

## drive con add attribute
drive_con = pm.PyNode("drive_C0_ctl")
drive_con.addAttr("steering", type="float", keyable=True, defaultValue=0)

# scale mul 
world_con = pm.PyNode("world_ctl")
world_con.addAttr("size", type="float", keyable=True, defaultValue=1)
world_con.size >> world_con.sx
world_con.size >> world_con.sy
world_con.size >> world_con.sz

world_con.sx.lock(True)
world_con.sx.setKeyable(False)
world_con.sy.lock(True)
world_con.sy.setKeyable(False)
world_con.sz.lock(True)
world_con.sz.setKeyable(False)

host_root = pm.PyNode("carUI_C0_root")
host_con = host_root.replace("root", "ctl")


drive_root = pm.PyNode("drive_C0_root")
ball_root = pm.PyNode("ball_L0_root")
ball_end_root = pm.PyNode("ballEnd_L0_root")
wheel_root = pm.PyNode("wheel_L0_root")
wheel_rig(index="L0", hostui=host_root, drive=drive_root, ball=ball_root, ballEnd=ball_end_root, wheel=wheel_root, direction=True)

ball_root = pm.PyNode("ball_R0_root")
ball_end_root = pm.PyNode("ballEnd_R0_root")
wheel_root = pm.PyNode("wheel_R0_root")
wheel_rig(index="R0", hostui=host_root, drive=drive_root, ball=ball_root, ballEnd=ball_end_root, wheel=wheel_root, direction=True)

ball_root = pm.PyNode("ball_L1_root")
ball_end_root = pm.PyNode("ballEnd_L1_root")
wheel_root = pm.PyNode("wheel_L1_root")
wheel_rig(index="L1", hostui=host_root, drive=drive_root, ball=ball_root, ballEnd=ball_end_root, wheel=wheel_root, direction=True)

ball_root = pm.PyNode("ball_R1_root")
ball_end_root = pm.PyNode("ballEnd_R1_root")
wheel_root = pm.PyNode("wheel_R1_root")
wheel_rig(index="R1", hostui=host_root, drive=drive_root, ball=ball_root, ballEnd=ball_end_root, wheel=wheel_root, direction=True)


