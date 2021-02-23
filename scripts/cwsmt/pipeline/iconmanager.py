# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

def maya_main_window():
    mainPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mainPtr), QtWidgets.QWidget)

class IconManager(QtWidgets.QDialog):

    ui_name = "iconManagerUI"
    DEFAULT_PATH = "{0}icons".format(mc.internalVar(upd=True))

    def __init__(self, parent=maya_main_window()):
        super(IconManager, self).__init__(parent=parent)

        self.setObjectName(self.ui_name)
        self.setWindowTitle("Icon Manager")

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.set_icon()

    def create_widgets(self):
        self.filter_line = QtWidgets.QLineEdit()
        self.search_btn = QtWidgets.QPushButton("search")

        self.icon_list = QtWidgets.QListWidget()
        self.icon_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.icon_list.setSpacing(2)
        self.icon_list.setViewMode(QtWidgets.QListView.IconMode)
        self.icon_list.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustToContents)
        self.icon_list.setIconSize(QtCore.QSize(48, 48))
        self.icon_list.setDragEnabled(False)

        self.name_line = QtWidgets.QLineEdit()
        self.name_line.setReadOnly(True)

        QtWidgets.QShortcut(QtGui.QKeySequence("enter"), self.search_btn, self.set_icon)
        QtWidgets.QShortcut(QtGui.QKeySequence("return"), self.search_btn, self.set_icon)

    def create_layouts(self):   
        main_layout = QtWidgets.QGridLayout(self)
        filter_layout = QtWidgets.QFormLayout()
        filter_layout.addRow("name_filter :", self.filter_line)

        main_layout.addLayout(filter_layout, 0, 0)
        main_layout.addWidget(self.search_btn, 0, 1)

        main_layout.addWidget(self.icon_list, 2, 0, 1, 2)
        name_layout = QtWidgets.QFormLayout()
        name_layout.addRow("name :", self.name_line)
        main_layout.addLayout(name_layout, 3, 0, 1, 2)

    def create_connections(self):
        self.search_btn.clicked.connect(self.set_icon)
        self.icon_list.itemClicked.connect(self.print_name)

    def set_icon(self): 
        if self.filter_line.text() == "":
            name_filter = "*"
        else:
            name_filter = "*{0}*".format(self.filter_line.text())
        
        images = mc.resourceManager(nameFilter=name_filter)
        self.icon_list.clear()
        if images == None:
            return

        for image in images:
            image_path = ":/{0}".format(image)
            image = QtGui.QImage(image_path)
            image = image.scaled(32, 32, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image)
            
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(pixmap), None)
            item.setSizeHint(QtCore.QSize(32, 32))
            item.setToolTip(image_path)   

            self.icon_list.addItem(item)

    def print_name(self):
        self.name_line.setText(self.icon_list.currentItem().toolTip())

    @classmethod
    def display(cls):
        if mc.window(cls.ui_name, query=True, exists=True):
            mc.deleteUI(cls.ui_name)
        ui = cls()
        ui.show() 

if __name__ == "__main__":
    IconManager.display()