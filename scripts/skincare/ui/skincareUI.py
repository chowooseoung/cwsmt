#-*- coding:utf-8 -*-

import maya.cmds as mc
import maya.mel as mel
import maya.OpenMayaUI as omui

import skincare.core.skincare as sc
reload(sc)

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

def maya_main_window():
    mayaWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)

class UndoWith():

    def __enter__(self):
        mc.undoInfo(ock=1)

    def __exit__(self, *args):
        mc.undoInfo(cck=1)


class SkincareUI(QtWidgets.QDialog):
    
    UINAME = "skincareUI"

    def __init__(self, parent=maya_main_window()):
        super(SkincareUI, self).__init__(parent)

        self.setObjectName(SkincareUI.UINAME)
        self.setWindowTitle("skincare")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.orig = []
        self.new = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.leftListGroupBox = QtWidgets.QGroupBox("Left List")
        self.leftListWidget = QtWidgets.QListWidget()
        self.rightListGroupBox = QtWidgets.QGroupBox("Right List")
        self.rightListWidget = QtWidgets.QListWidget()

        self.leftSelectBtn = QtWidgets.QPushButton("select!")
        self.rightSelectBtn = QtWidgets.QPushButton("select!")
        self.leftToRightBtn = QtWidgets.QPushButton(">>")
        self.leftToRightBtn.setFixedSize(20,20)

        self.leftSelectComboBox = QtWidgets.QComboBox()
        self.selectItem = ["mesh", "nurbsSurface", "nurbsCurve", "locator", "joint", "transform"]
        self.leftSelectComboBox.addItems(self.selectItem)
        self.rightSelectComboBox = QtWidgets.QComboBox()
        self.rightSelectComboBox.addItems(self.selectItem)

        self.modeGroupBox = QtWidgets.QGroupBox("Mode")
        self.exportRadioBtn = QtWidgets.QRadioButton("export")
        self.importRadioBtn = QtWidgets.QRadioButton("import")
        self.copyRadioBtn = QtWidgets.QRadioButton("copy")
        self.copyRadioBtn.setChecked(1)

        self.copyMethodGroupBox = QtWidgets.QGroupBox("Copy Method")
        self.moveJointRadioBtn = QtWidgets.QRadioButton("move")
        self.moveJointRadioBtn.setChecked(1)
        self.namespaceCheckBtn = QtWidgets.QCheckBox("namespace")
        self.onetomanyRadioBtn = QtWidgets.QRadioButton("1 : N")
        self.manytooneRadioBtn = QtWidgets.QRadioButton("N : 1")
        self.manytomanyRadioBtn = QtWidgets.QRadioButton("N : N")

        self.pathGroupBox = QtWidgets.QGroupBox("Path")
        self.pathBtn = QtWidgets.QPushButton("Path")
        self.openPathBtn = QtWidgets.QPushButton("P")
        self.openPathBtn.setFixedSize(20,20)

        self.goBtn = QtWidgets.QPushButton("go!")

    def create_layouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        listWidgetLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(listWidgetLayout)
        leftListGroupBoxLayout = QtWidgets.QVBoxLayout(self.leftListGroupBox)
        rightListGroupBoxLayout = QtWidgets.QVBoxLayout(self.rightListGroupBox)
        listWidgetLayout.addWidget(self.leftListGroupBox)
        listWidgetLayout.addWidget(self.leftToRightBtn)
        listWidgetLayout.addWidget(self.rightListGroupBox)

        leftListGroupBoxLayout.addWidget(self.leftListWidget)
        leftSelectLayout = QtWidgets.QHBoxLayout()
        leftListGroupBoxLayout.addLayout(leftSelectLayout)
        leftSelectLayout.addWidget(self.leftSelectComboBox)
        leftSelectLayout.addWidget(self.leftSelectBtn)
        
        rightListGroupBoxLayout.addWidget(self.rightListWidget)
        rightSelectLayout = QtWidgets.QHBoxLayout()
        rightListGroupBoxLayout.addLayout(rightSelectLayout)
        rightSelectLayout.addWidget(self.rightSelectComboBox)
        rightSelectLayout.addWidget(self.rightSelectBtn)
        
        modeGroupBoxLayout = QtWidgets.QHBoxLayout(self.modeGroupBox)
        mainLayout.addWidget(self.modeGroupBox)
        modeGroupBoxLayout.addWidget(self.exportRadioBtn)
        modeGroupBoxLayout.addWidget(self.importRadioBtn)
        modeGroupBoxLayout.addWidget(self.copyRadioBtn)

        copyMethodGroupLayout = QtWidgets.QVBoxLayout(self.copyMethodGroupBox)
        mainLayout.addWidget(self.copyMethodGroupBox)
        copyMethodGroupLayout1 = QtWidgets.QGridLayout()
        copyMethodGroupLayout.addLayout(copyMethodGroupLayout1)

        copyMethodGroupLayout1.addWidget(self.moveJointRadioBtn, 0,0)
        copyMethodGroupLayout1.addWidget(self.namespaceCheckBtn, 0,2)
        copyMethodGroupLayout1.addWidget(self.onetomanyRadioBtn, 1,0)
        copyMethodGroupLayout1.addWidget(self.manytooneRadioBtn, 1,1)
        copyMethodGroupLayout1.addWidget(self.manytomanyRadioBtn, 1,2)

        pathGroupLayout = QtWidgets.QHBoxLayout(self.pathGroupBox)
        mainLayout.addWidget(self.pathGroupBox)
        pathGroupLayout.addWidget(self.pathBtn)
        pathGroupLayout.addWidget(self.openPathBtn)

        mainLayout.addWidget(self.goBtn)

    def create_connections(self):
        self.leftSelectBtn.clicked.connect(self.left_list_select)
        self.rightSelectBtn.clicked.connect(self.right_list_select)
        self.leftToRightBtn.clicked.connect(self.left_to_right)
        self.goBtn.clicked.connect(self.go)

    def left_list_select(self):
        with UndoWith():
            selection = mc.ls(sl=1)
            if len(selection) == []:
                return
            self.orig = []
            for i in selection:
                if mc.listRelatives(i, s=1):
                    if mc.nodeType(mc.listRelatives(i, s=1)[0]) == self.leftSelectComboBox.currentText():
                        if sc.get_skin_node(i):
                            self.orig.append(i)
            mc.select(self.orig)
            self.refresh_list()

    def right_list_select(self):
        with UndoWith():
            selection = mc.ls(sl=1)
            if len(selection) == []:
                return
            self.new = []
            for i in selection:
                if mc.listRelatives(i, s=1):
                    if mc.nodeType(mc.listRelatives(i, s=1)[0]) == self.rightSelectComboBox.currentText():
                        self.new.append(i)
                elif not mc.listRelatives(i, s=1):
                    if mc.nodeType(i) == self.rightSelectComboBox.currentText():
                        self.new.append(i)
            mc.select(self.new)
            self.refresh_list()

    def left_to_right(self):
        self.new = []
        for i in self.orig:
            if ":" in i:
                if i.split(":")[-1] not in self.new:
                    self.new.append(i.split(":")[-1])
        self.refresh_list()

    def refresh_list(self):
        check = False
        item = []
        for i in self.new:
            if not mc.objExists(i):
                check = True
                item.append(i)
        for i in item:
            self.new.remove(i)

        self.leftListWidget.clear()
        self.rightListWidget.clear()
        leftNumber = "len : {0}".format(len(self.orig))
        rightNumber = "len : {0}".format(len(self.new))
        self.leftListWidget.addItems(self.orig)
        self.leftListWidget.addItem("")
        self.leftListWidget.addItem(leftNumber)
        self.rightListWidget.addItems(self.new)
        self.rightListWidget.addItem("")
        self.rightListWidget.addItem(rightNumber)

        if check:
            self.rightListWidget.addItem("")
            self.rightListWidget.addItem("=== Item not in this scene ===")
            self.rightListWidget.addItems(item)

    def go(self):
        with UndoWith():
            if self.copyRadioBtn.isChecked():
                if self.onetomanyRadioBtn.isChecked():
                    sc.o_n_copy(orig=self.orig, new=self.new, ref=self.namespaceCheckBtn.isChecked())
                elif self.manytooneRadioBtn.isChecked():
                    sc.n_o_copy(orig=self.orig, new=self.new, ref=self.namespaceCheckBtn.isChecked())
                elif self.manytomanyRadioBtn.isChecked():
                    sc.n_n_copy(orig=self.orig, new=self.new, ref=self.namespaceCheckBtn.isChecked())
                elif self.moveJointRadioBtn.isChecked():
                    sc.move_joint(objName=self.orig)    
                    
    @classmethod
    def display(cls):
        with UndoWith():
            if mc.window(SkincareUI.UINAME, query=True, exists=True):
                mc.deleteUI(SkincareUI.UINAME)
            ui = SkincareUI()
            ui.show()

if __name__ == "__main__":
    SkincareUI.display()