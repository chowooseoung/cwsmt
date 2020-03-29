import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel

import os
import sys

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

def maya_main_window():
    mainPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mainPtr), QtWidgets.QWidget)

class IconManager(QtWidgets.QDialog):

    UINAME = "iconManager"
    DEFAULT_PATH = "{0}icons".format(mc.internalVar(upd=True))

    def __init__(self, parent=maya_main_window()):
        super(IconManager, self).__init__(parent=parent)

        self.setObjectName(IconManager.UINAME)
        self.setWindowTitle(IconManager.UINAME)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.set_icon()

    def create_widgets(self):
        self.filterLine = QtWidgets.QLineEdit()
        self.searchBtn = QtWidgets.QPushButton("search")

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["maya default", "path {0}".format(IconManager.DEFAULT_PATH)])
        
        self.iconList = QtWidgets.QListWidget()
        self.iconList.setResizeMode(QtWidgets.QListView.Adjust)
        self.iconList.setSpacing(2)
        self.iconList.setViewMode(QtWidgets.QListView.IconMode)
        self.iconList.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustToContents)
        self.iconList.setIconSize(QtCore.QSize(48, 48))
        self.iconList.setDragEnabled(False)

        self.nameLine = QtWidgets.QLineEdit()
        self.nameLine.setReadOnly(True)

    def create_layouts(self):   
        mainLayout = QtWidgets.QGridLayout(self)
        filterLayout = QtWidgets.QFormLayout()
        filterLayout.addRow("nameFilter :", self.filterLine)

        mainLayout.addLayout(filterLayout, 0, 0)
        mainLayout.addWidget(self.searchBtn, 0, 1)

        mainLayout.addWidget(self.combo, 1, 0, 1, 2)
        mainLayout.addWidget(self.iconList, 2, 0, 1, 2)
        nameLayout = QtWidgets.QFormLayout()
        nameLayout.addRow("name :", self.nameLine)
        mainLayout.addLayout(nameLayout, 3, 0, 1, 2)

    def create_connections(self):
        self.searchBtn.clicked.connect(self.set_icon)
        self.iconList.itemClicked.connect(self.print_name)

    def set_icon(self): 
        if self.filterLine.text() == "":
            nameFilter = "*"
        else:
            nameFilter = "*{0}*".format(self.filterLine.text())
        
        if self.combo.currentIndex() == 0:
            image = mc.resourceManager(nf=nameFilter)
            if image == None:
                self.iconList.clear()
                return
            self.iconList.clear()

            for i in image:
                path = ":{0}".format(i)
                image = QtGui.QImage(path)
                image = image.scaled(32, 32, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(image)
                
                item = QtWidgets.QListWidgetItem(QtGui.QIcon(pixmap), None)
                item.setSizeHint(QtCore.QSize(32, 32))
                item.setToolTip(path)   

                self.iconList.addItem(item)

        elif self.combo.currentIndex() == 1:
            print 'b'

    def print_name(self):
        self.nameLine.setText(self.iconList.currentItem().toolTip())

    @classmethod
    def display(cls):
        if mc.window(cls.UINAME, query=True, exists=True):
            mc.deleteUI(cls.UINAME)
        ui = IconManager()
        ui.show()

if __name__ == "__main__":
    IconManager.display()