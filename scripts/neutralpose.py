# -*- coding:utf-8 -*-

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import pymel.core as pm
import maya.OpenMayaUI as omui


def neutral_pose(addname, snap=False, child=False, objType=None, lastIndex=False):
    selected_nodes = pm.ls(selection=True)
    
    if not selected_nodes:
        return

    name_list = list() 
    for index in range(len(selected_nodes)):
        if lastIndex == True:
            temp_name_list = selected_nodes[index].name().split("_")
            temp_name_list.pop(-1)
            edit_name = "_".join(temp_name_list)
            name_list.append("{0}_{1}".format(edit_name, addname))
        else:
            name_list.append("{0}_{1}".format(selected_nodes[index].name(), addname))
        
        if pm.objExists(name_list[index]):
            pm.warning("already {0} exists".format(name_list[index]))
            return
    
    zeroout_grp = []
    for index in range(len(selected_nodes)):
        parent_name = selected_nodes[index].getParent()
        name = name_list[index]
        
        if objType == "transform":
            zeroout_grp.append(pm.group(empty=True, name=name))
        elif objType == "joint":
            zeroout_grp.append(pm.createNode("joint", name=name))
        elif objType == "locator":
            zeroout_grp.append(pm.spaceLocator(name=name))
        elif objType == "cube":
            zeroout_grp.append(pm.curve(degree=1, point=([-1.0, 1.0, 1.0],
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
            zeroout_grp[index].rename(name)
        zeroout_grp[index].rotateOrder.set(selected_nodes[index].rotateOrder.get())

        pm.matchTransform(zeroout_grp[index], selected_nodes[index])
        if snap == False:
            if child == False:
                if parent_name == None:
                    pm.parent(selected_nodes[index], zeroout_grp[index])
                else:
                    pm.parent(zeroout_grp[i], parent_name)
                    pm.parent(selected_nodes[index], zeroout_grp[index])
            else:
                pm.parent(zeroout_grp[index], selected_nodes[index])
    pm.select(zeroout_grp)
    return zeroout_grp


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
        self.groupBox = QtWidgets.QGroupBox()

        self.defaultRadioBtn = QtWidgets.QRadioButton("default")
        self.defaultRadioBtn.setChecked(True)
        self.snapRadioBtn = QtWidgets.QRadioButton("snap")
        self.childRadioBtn = QtWidgets.QRadioButton("child")
        self.lastIndexCheckBox = QtWidgets.QCheckBox("last index")

        self.nameLine = QtWidgets.QLineEdit()

        self.objTypeComboBox = QtWidgets.QComboBox()
        self.objTypeComboBox.addItems(self.objType)
        self.zeroOutBtn = QtWidgets.QPushButton("zero out")

    def create_layouts(self):
        mainLayout = QtWidgets.QFormLayout(self)

        groupBoxLayout = QtWidgets.QHBoxLayout(self.groupBox)
        groupBoxLayout.setContentsMargins(0,0,0,0)
        groupBoxLayout.addWidget(self.defaultRadioBtn)
        groupBoxLayout.addWidget(self.snapRadioBtn)
        groupBoxLayout.addWidget(self.childRadioBtn)
        groupBoxLayout.addWidget(self.lastIndexCheckBox)
        mainLayout.addRow(self.groupBox)
        mainLayout.addRow("suffix name: ", self.nameLine)

        createLayout = QtWidgets.QHBoxLayout()
        createLayout.addWidget(self.objTypeComboBox)
        createLayout.addWidget(self.zeroOutBtn)
        mainLayout.addRow(createLayout)

    def create_connections(self):
        self.zeroOutBtn.clicked.connect(self.zero_out)

    @undo_info
    def zero_out(self):
        name = self.nameLine.text()
        snap = self.snapRadioBtn.isChecked()
        child = self.childRadioBtn.isChecked()
        objType = self.objTypeComboBox.currentText()
        lastIndex = self.lastIndexCheckBox.isChecked()
        if name == "":
            name = "GRP"
        
        neutral_pose(addname=name, snap=snap, child=child, objType=objType, lastIndex=lastIndex)

    @classmethod
    @undo_info
    def display(cls):
        if pm.window(cls.ui_name, query=True, exists=True):
            pm.deleteUI(cls.ui_name)
        ui = cls()
        ui.show()

if __name__ == "__main__":
    NeutralPoseUI.display()