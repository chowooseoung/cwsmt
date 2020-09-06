from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import pymel.core as pm
import maya.OpenMayaUI as omui

def maya_main_window():
    mayaWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)

def undoInfo(func):
    def wrapper(*args, **kwargs):
        pm.undoInfo(ock=1)
        funcVar = func(*args, **kwargs)
        pm.undoInfo(cck=1)
        return funcVar
    return wrapper

class Renamer():

    def __init__(self, orig=None, new=None, selection=None, padding=None, number=None):
        self.set_value(orig=orig, new=new, selection=selection, padding=padding, number=number)

    def prefix(self):
        for i in self.selection:
            name = i.addPrefix('{0}'.format(self.new))
            if pm.ls('{0}'.format(name)):
                new = i.rename(name)
                pm.warning('{0} already exists. *** result : {1} ***'.format(name, new))
            else:
                i.rename(name)

    def suffix(self):
        for i in self.selection:
            name = '{0}{1}'.format(i.name(), self.new)
            if pm.ls('{0}'.format(name)):
                new = i.rename(name)
                pm.warning('{0} already exists. *** result : {1} ***'.format(name, new))
            else:
                i.rename(name)

    def search_replace(self):
        for i in self.selection:
            name = i.replace(self.orig, self.new)
            if pm.ls('{0}'.format(name)):
                new = i.rename(name)
                pm.warning('{0} already exists. *** result : {1} ***'.format(name, new))
            else:
                i.rename(name)

    def renaming(self):
        for i in self.selection:
            name = '{0}{1}'.format(self.new, str(self.number).zfill(self.padding))
            if pm.ls('{0}'.format(name)):
                new = i.rename(name)
                pm.warning('{0} already exists. *** result : {1} ***'.format(name, new))
            else:
                i.rename(name)
            self.number += 1

    def set_value(self, **args):
        if args.has_key("orig"):
            self.orig = args["orig"]
        if args.has_key("new"):
            self.new = args["new"]   
        if args.has_key("selection"):
            self.selection = args["selection"]
        if args.has_key("padding"):
            if args["padding"] != None:
                self.padding = int(args["padding"])
        if args.has_key("number"):
            if args["number"] != None:
                self.number = int(args["number"])


class RenamerUI(QtWidgets.QDialog):

    ui_name = "namingUI"

    def __init__(self, parent=maya_main_window()):
        super(RenamerUI, self).__init__(parent)

        self.setObjectName(self.ui_name)
        self.setWindowTitle(self.ui_name)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300,140)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.na = Renamer()

    def create_widgets(self):
        self.orig_line = QtWidgets.QLineEdit()
        self.new_line = QtWidgets.QLineEdit()
        self.number_line = QtWidgets.QLineEdit()
        self.number_line.setText('0')
        self.padding_line = QtWidgets.QLineEdit()
        self.padding_line.setText('0')
        
        self.prefix_btn = QtWidgets.QPushButton("prefix")
        self.suffix_btn = QtWidgets.QPushButton("suffix")
        self.search_replace_btn = QtWidgets.QPushButton("search replace")
        self.renaming_btn = QtWidgets.QPushButton("renaming")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        
        orig_line_layout = QtWidgets.QFormLayout()
        orig_line_layout.addRow("orig", self.orig_line)

        new_line_layout = QtWidgets.QFormLayout()
        new_line_layout.addRow("new", self.new_line)

        top_line_layout = QtWidgets.QHBoxLayout()
        top_line_layout.addLayout(orig_line_layout)
        top_line_layout.addLayout(new_line_layout)
        main_layout.addLayout(top_line_layout)

        top_btn_layout = QtWidgets.QHBoxLayout()
        top_btn_layout.addWidget(self.prefix_btn)
        top_btn_layout.addWidget(self.suffix_btn)
        top_btn_layout.addWidget(self.search_replace_btn)
        main_layout.addLayout(top_btn_layout)

        padding_line_layout = QtWidgets.QFormLayout()
        padding_line_layout.addRow("padding", self.padding_line)

        number_line_layout = QtWidgets.QFormLayout()
        number_line_layout.addRow("number", self.number_line)

        bottom_line_layout = QtWidgets.QHBoxLayout()
        bottom_line_layout.addLayout(number_line_layout)
        bottom_line_layout.addLayout(padding_line_layout)
        main_layout.addLayout(bottom_line_layout)

        main_layout.addWidget(self.renaming_btn)
        
    def create_connections(self):
        self.prefix_btn.clicked.connect(self.prefix)
        self.suffix_btn.clicked.connect(self.suffix)
        self.search_replace_btn.clicked.connect(self.search_replace)
        self.renaming_btn.clicked.connect(self.renaming)

    @undoInfo
    def prefix(self):
        self.na.set_value(new=self.new_line.text(), selection=pm.ls(selection=True))
        self.na.prefix()

    @undoInfo
    def suffix(self):
        self.na.set_value(new=self.new_line.text(), selection=pm.ls(selection=True))
        self.na.suffix()

    @undoInfo
    def search_replace(self):
        if self.orig_line.text() == "":
            return
        self.na.set_value(orig=self.orig_line.text(), new=self.new_line.text()
                            , selection=pm.ls(selection=True))
        self.na.search_replace()

    @undoInfo
    def renaming(self):
        try:
            int(self.number_line.text())
            int(self.padding_line.text())
        except:
            pm.warning("number and padding need int type") 
            return
        if not self.new_line.text():
            return
        elif int(self.number_line.text()) < 0:
            pm.warning("number >= 0") 
            return
        elif int(self.padding_line.text()) < 0:
            pm.warning("padding >= 0") 
            return
        self.na.set_value(new=self.new_line.text(), number=self.number_line.text(), 
                            padding=self.padding_line.text(), selection=pm.ls(selection=True))
        self.na.renaming()
            
    @classmethod
    @undoInfo
    def display(cls):
        if pm.window(cls.ui_name, query=True, exists=True):
            pm.deleteUI(cls.ui_name)
        ui = cls()
        ui.show()

if __name__ == "__main__":
    RenamerUI.display()