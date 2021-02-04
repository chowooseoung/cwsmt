# cmt
from cmt.rig.meshretarget import *
import cmt.shortcuts as shortcuts

# maya
import pymel.core as pm
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

# numpy
import numpy as np

# scipy
from scipy.spatial.distance import cdist

# 
import math
import time

guides = ("body_C0_root",
"shoulder_L0_root",
"shoulder_R0_root",
"shoulder_L0_tip",
"shoulder_R0_tip",
"arm_L0_elbow",
"arm_R0_elbow",
"arm_L0_wrist",
"arm_R0_wrist",
"arm_L0_eff",
"arm_R0_eff",
"meta_L0_root",
"meta_R0_root",
"meta_L0_0_loc",
"meta_R0_0_loc",
"meta_L0_1_loc",
"meta_R0_1_loc",
"meta_L0_2_loc",
"meta_R0_2_loc",
"thumbRoll_L0_root",
"thumbRoll_R0_root",
"thumb_L0_0_loc",
"thumb_R0_0_loc",
"thumb_L0_1_loc",
"thumb_R0_1_loc",
"thumb_L0_2_loc",
"thumb_R0_2_loc",
"finger_L0_root",
"finger_R0_root",
"finger_L0_0_loc",
"finger_R0_0_loc",
"finger_L0_1_loc",
"finger_R0_1_loc",
"finger_L0_2_loc",
"finger_R0_2_loc",
"finger_L1_root",
"finger_R1_root",
"finger_L1_0_loc",
"finger_R1_0_loc",
"finger_L1_1_loc",
"finger_R1_1_loc",
"finger_L1_2_loc",
"finger_R1_2_loc",
"finger_L2_root",
"finger_R2_root",
"finger_L2_0_loc",
"finger_L2_0_loc",
"finger_L2_1_loc",
"finger_L2_1_loc",
"finger_L2_2_loc",
"finger_L2_2_loc",
"finger_L3_root",
"finger_L3_0_loc",
"finger_L3_0_loc",
"finger_L3_1_loc",
"finger_L3_1_loc",
"finger_L3_2_loc",
"finger_L3_2_loc",
"leg_L0_root",
"leg_R0_root",
"leg_L0_knee",
"leg_R0_knee",
"leg_L0_ankle",
"leg_R0_ankle",
"foot_L0_heel",
"foot_R0_heel",
"foot_L0_inpivot",
"foot_R0_inpivot",
"foot_L0_outpivot",
"foot_R0_outpivot",
"foot_L0_0_loc",
"foot_R0_0_loc",
"leg_L0_eff",
"leg_R0_eff",
"foot_L0_1_loc",
"foot_R0_1_loc",)

def retarget(source, target, rbf=None, radius=0.5, stride=1):
    """Run the mesh retarget.
    :param source: Source mesh
    :param target: Modified source mesh
    :param shapes: List of meshes to retarget
    :param rbf: One of the RBF functions. See class RBF
    :param radius: Smoothing parameter for the rbf
    :param stride: Vertex stride to sample on the source mesh.  Increase to speed up
    the calculation but less accurate.
    """
    start_time = time.time()
    source_points = points_to_np_array(source, stride)
    target_points = points_to_np_array(target, stride)

    if rbf is None:
        rbf = RBF.linear
    weights = get_weight_matrix(source_points, target_points, rbf, radius)

    points = get_guide_points()
    n_points = points.shape[0]
    dist = get_distance_matrix(points, source_points, rbf, radius)
    identity = np.ones((n_points, 1))
    h = np.bmat([[dist, identity, points]])
    deformed = np.asarray(np.dot(h, weights))
    points = [OpenMaya.MPoint(*p) for p in deformed]
    set_guide_points(points)

    end_time = time.time()
    print("Transferred in {} seconds".format(end_time - start_time))


def get_guide_points(stride=1):
    points = [ pm.xform(guide, query=True, translation=True, worldSpace=True) for guide in guides]
    sparse_points = [OpenMaya.MPoint(p) for p in points][::stride]
    np_points = np.array([[p.x, p.y, p.z] for p in sparse_points])
    return np_points

def set_guide_points(points):
    for index, point in enumerate(points):
        pm.xform(guides[index], translation=point, worldSpace=True)

retarget(pm.ls(sl=1)[0], pm.ls(sl=1)[1])