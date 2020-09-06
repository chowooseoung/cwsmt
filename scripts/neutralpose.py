# -*- coding:utf-8 -*-

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import pymel.core as pm
import maya.OpenMayaUI as omui


def neutral_pose(addName, snap=False, child=False, objType=None, lastIndex=False):
    selected_nodes = pm.ls(selection=True)
    
    if not selected_nodes:
        return

    name_list = list() 
    for index in range(len(selected_nodes)):
        if lastIndex == True:
            temp_name_list = selected_nodes[index].name().split("_")
            temp_name_list.pop(-1)
            edit_name = "_".join(temp_name_list)
            name_list.append("{0}{1}".format(edit_name, addName))
        else:
            name_list.append("{0}{1}".format(selected_nodes[index].name(), addName))
        
        if pm.objExists(name_list[index]):
            pm.warning("already {0} exists".format(name_list[index]))
            return
    
    neutral_pose_grp = list()
    for index in range(len(selected_nodes)):
        parent_name = selected_nodes[index].getParent()
        name = name_list[index]
        
        if objType == "transform":
            neutral_pose_grp.append(pm.group(empty=True, name=name))
        elif objType == "joint":
            neutral_pose_grp.append(pm.createNode("joint", name=name))
        elif objType == "locator":
            neutral_pose_grp.append(pm.spaceLocator(name=name))
        elif objType == "cube":
            neutral_pose_grp.append(pm.curve(degree=1, point=([-1.0, 1.0, 1.0],
                                                        [-1.0, 1.0, -1.0],
                                                        [1.0, 1.0, -1.0],
                                                        [1.0, 1.0, 1.0],
                                                        [-1.0, 1.0, 1.0],
                                                        [-1.0, -1.0, 1.0],
                                                        [1.0, -1.0, 1.0],
                                                        [1.0, 1.0, 1.0],
                                                        [1.0, -1.0, 1.0],
                                                        [1.0, -1.0, -1.0],
                                                        [1.0, 1.0, -1.0],
                                                        [1.0, -1.0, -1.0],
                                                        [-1.0, -1.0, -1.0],
                                                        [-1.0, 1.0, -1.0],
                                                        [-1.0, -1.0, -1.0],
                                                        [-1.0, -1.0, 1.0])))
            neutral_pose_grp[index].rename(name)
        neutral_pose_grp[index].rotateOrder.set(selected_nodes[index].rotateOrder.get())

        pm.matchTransform(neutral_pose_grp[index], selected_nodes[index])
        if snap == False:
            if child == False:
                if parent_name == None:
                    pm.parent(selected_nodes[index], neutral_pose_grp[index])
                else:
                    pm.parent(neutral_pose_grp[i], parent_name)
                    pm.parent(selected_nodes[index], neutral_pose_grp[index])
            else:
                pm.parent(neutral_pose_grp[index], selected_nodes[index])
    pm.select(neutral_pose_grp)
    return neutral_pose_grp


def maya_main_window():
    mayaWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)


def undo_info(func):
    def wrapper(*args, **kwargs):
        pm.undoInfo(ock=True)
        var = func(*args, **kwargs)
        pm.undoInfo(cck=True)
        return var
    return wrapper


class NeutralPoseUI(QtWidgets.QDialog):

    ui_name = "NeutralPoseUI"

    def __init__(self, parent=maya_main_window()):
        super(NeutralPoseUI, self).__init__(parent=parent)

        self.setObjectName(self.ui_name)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("NeutralPose")

        self.objType = ["transform", "joint", "locator", "cube"]

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.group_box = QtWidgets.QGroupBox()

        self.default_radio_btn = QtWidgets.QRadioButton("default")
        self.default_radio_btn.setChecked(True)
        self.snap_radio_btn = QtWidgets.QRadioButton("snap")
        self.child_radio_btn = QtWidgets.QRadioButton("child")
        self.last_index_check_box = QtWidgets.QCheckBox("last index")

        self.name_line = QtWidgets.QLineEdit()

        self.obj_type_combo_box = QtWidgets.QComboBox()
        self.obj_type_combo_box.addItems(self.objType)
        self.neutral_pose_btn = QtWidgets.QPushButton("zero out")

    def create_layouts(self):
        main_layout = QtWidgets.QFormLayout(self)

        group_box_layout = QtWidgets.QHBoxLayout(self.group_box)
        group_box_layout.setContentsMargins(0,0,0,0)
        group_box_layout.addWidget(self.default_radio_btn)
        group_box_layout.addWidget(self.snap_radio_btn)
        group_box_layout.addWidget(self.child_radio_btn)
        group_box_layout.addWidget(self.last_index_check_box)
        main_layout.addRow(self.group_box)
        main_layout.addRow("suffix name: ", self.name_line)

        create_layout = QtWidgets.QHBoxLayout()
        create_layout.addWidget(self.obj_type_combo_box)
        create_layout.addWidget(self.neutral_pose_btn)
        main_layout.addRow(create_layout)

    def create_connections(self):
        self.neutral_pose_btn.clicked.connect(self.neutral_pose_click)

    @undo_info
    def neutral_pose_click(self):
        name = self.name_line.text()
        snap = self.snap_radio_btn.isChecked()
        child = self.child_radio_btn.isChecked()
        objType = self.obj_type_combo_box.currentText()
        lastIndex = self.last_index_check_box.isChecked()
        if not name:
            name = "_GRP"
        
        neutral_pose(addName=name, snap=snap, child=child, objType=objType, lastIndex=lastIndex)

    @classmethod
    @undo_info
    def display(cls):
        if pm.window(cls.ui_name, query=True, exists=True):
            pm.deleteUI(cls.ui_name)
        ui = cls()
        ui.show()

if __name__ == "__main__":
    NeutralPoseUI.display()