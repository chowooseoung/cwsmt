import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel

import os
import sys

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from functools import partial

def maya_main_window():
    mainPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mainPtr), QtWidgets.QWidget)

class IconName(QtWidgets.QDialog):

    UINAME = "ICONNAME"

    def __init__(self, parent=maya_main_window()):
        super(IconName, self).__init__(parent=parent)

        self.setObjectName(IconName.UINAME)
        self.setWindowTitle(IconName.UINAME)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.set_icon()

    def create_widgets(self):
        self.iconList = QtWidgets.QListWidget()
        # self.iconList.setFlow(QtWidgets.QListView.LeftToRight)
        self.iconList.setResizeMode(QtWidgets.QListView.Adjust)
        # self.iconList.setGridSize(QtCore.QSize(64, 64))
        self.iconList.setSpacing(2)
        self.iconList.setViewMode(QtWidgets.QListView.IconMode)
        self.iconList.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustToContents)

    def create_layouts(self):
        mainLayout = QtWidgets.QGridLayout(self)
        mainLayout.addWidget(self.iconList, 0, 0)
        
    def create_connections(self):
        pass

    def set_icon(self):
        for i in mc.resourceManager():
            path = ":{0}".format(i)
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(path))
            btn.setIconSize(QtCore.QSize(32, 32))
            btn.setToolTip(path)
            btn.clicked.connect(partial(self.print_name, path))

            item = QtWidgets.QListWidgetItem(self.iconList)
            item.setSizeHint(btn.sizeHint())
            self.iconList.setItemWidget(item, btn)

    def print_name(self, name):
        print name

    @classmethod
    def display(cls):
        if mc.window(cls.UINAME, query=True, exists=True):
            mc.deleteUI(cls.UINAME)
        ui = IconName()
        ui.show()

if __name__ == "__main__":
    IconName.display()