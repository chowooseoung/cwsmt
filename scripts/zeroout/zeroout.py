#-*- coding:utf-8 -*-

import maya.cmds as mc
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance


def do_zeroout(addname="GRP", snap=False, child=False, objType="transfrom", lastindex=False):
    '''
    zeroout

    return: zerooutGRP
    '''
    suffixName = "_{0}".format(addname)
    selection = mc.ls(sl=True)
    
    nameList = []    
    for i in range(len(selection)):
        if lastindex == True:
            temp = selection[i].split("_")
            temp.pop(-1)
            removeIndexName = "_".join(temp)
            nameList.append("{0}{1}".format(removeIndexName, suffixName))
        else:
            nameList.append("{0}{1}".format(selection[i], suffixName))
        
        if mc.objExists(nameList[i]):
            mc.warning("already {0} exists".format(nameList[i]))
            return
    
    zerooutGrp = []
    for i in range(len(selection)):
        parentName = mc.listRelatives(selection[i], p=True)
        name = nameList[i]
        
        if objType == "transform":
            zerooutGrp.append(mc.group(em=True, n=name))
        elif objType == "joint":
            zerooutGrp.append(mc.createNode("joint", n=name))
        elif objType == "locator":
            zerooutGrp.append(mc.spaceLocator(n=name)[0])
        elif objType == "cube":
            temp = mc.curve(d=1, p=([-1.0, 1.0, 1.0],
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
                                    [-1.0, -1.0, 1.0]))
            zerooutGrp.append(mc.rename(temp, name))

        t = mc.xform(selection[i], q=True, t=True, ws=True)
        ro = mc.xform(selection[i], q=True, ro=True, ws=True)
        s = mc.xform(selection[i], q=True, s=True, ws=True)

        mc.xform(zerooutGrp[i], t=t, ws=True)
        mc.xform(zerooutGrp[i], ro=ro, ws=True)
        mc.xform(zerooutGrp[i], s=s, ws=True)
        if snap == False:
            if child == False:
                if parentName == None:
                    mc.parent(selection[i], zerooutGrp[i])
                else:
                    mc.parent(zerooutGrp[i], parentName[0])
                    mc.parent(selection[i], zerooutGrp[i])
            else:
                mc.parent(zerooutGrp[i], selection[i])
    mc.select(zerooutGrp)
    return zerooutGrp

def maya_main_window():
    mayaWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)

class UndoWith():
    
    def __enter__(self):
        mc.undoInfo(ock=True)

    def __exit__(self, *args):
        mc.undoInfo(cck=True)

class ZeroOutUI(QtWidgets.QDialog):

    UINAME = "zerooutUI"

    def __init__(self, parent=maya_main_window()):
        super(ZeroOutUI, self).__init__(parent)

        self.setObjectName(self.UINAME)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("zero out")

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

    def zero_out(self):
        with UndoWith():
            name = self.nameLine.text()
            snap = self.snapRadioBtn.isChecked()
            child = self.childRadioBtn.isChecked()
            objType = self.objTypeComboBox.currentText()
            lastIndex = self.lastIndexCheckBox.isChecked()
            if name == "":
                name = "GRP"
            
            if mc.ls(sl=1) == []:
                return
                
            do_zeroout(addname=name, snap=snap, child=child, objType=objType, lastindex=lastIndex)

    @classmethod
    def display(cls):
        with UndoWith():
            if mc.window(ZeroOutUI.UINAME, query=True, exists=True):
                mc.deleteUI(ZeroOutUI.UINAME)
            ui = ZeroOutUI()
            ui.show()

if __name__ == "__main__":
    ZeroOutUI.display()