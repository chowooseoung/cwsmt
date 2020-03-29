#-*- coding:utf-8 -*-

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui

def maya_main_window():
    mayaWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWindowPtr), QtWidgets.QWidget)

class UndoWith():

    def __enter__(self):
        mc.undoInfo(ock=1)

    def __exit__(self, *args):
        mc.undoInfo(cck=1)


class Naming():

    def __init__(self, orig=None, new=None, selection=None, padding=None, number=None):
        self.set_value(orig=orig, new=new, selection=selection, padding=padding, number=number)

    def prefix(self):
        if (self.new == None) or (self.selection == None):
            mc.warning("confirm set_value")
            return
        temp = []
        for i in self.selection:
            newName = "{0}{1}".format(self.new, i)
            mc.rename(i, newName)
            temp.append(newName)
        self.selection = temp

    def suffix(self):
        if (self.new == None) or (self.selection == None):
            mc.warning("confirm set_value")
            return
        temp = []
        for i in self.selection:
            newName = "{0}{1}".format(i, self.new)
            mc.rename(i, newName)
            temp.append(newName)
        self.selection = temp

    def search_replace(self):
        if (self.new == None) or (self.selection == None) or (self.orig == None):
            mc.warning("confirm set_value")
            return
        temp = []
        for i in self.selection:
            if self.orig in i:
                newName = i.replace(self.orig, self.new)
                mc.rename(i, newName)
                temp.append(newName)
        self.selection = temp

    def renaming(self):
        if (self.new == None) or (self.selection == None) or (self.number == None) or (self.padding == None):
            mc.warning("confirm set_value")
            return
        temp = []
        tempName = []
        for i in self.selection:
            tempName.append(mc.rename(i, "q1w2e3#"))

        for i in tempName:
            newName = "{0}{1}".format(self.new, str(self.number).zfill(self.padding))
            mc.rename(i, newName)
            self.number += 1
            temp.append(newName)
        self.selection = temp

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


class NamingUI(QtWidgets.QDialog):

    UINAME = "namingUI"

    def __init__(self, parent=maya_main_window()):
        super(NamingUI, self).__init__(parent)

        self.setObjectName(NamingUI.UINAME)
        self.setWindowTitle("Naming helper")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300,140)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.na = Naming()

    def create_widgets(self):
        self.origLine = QtWidgets.QLineEdit()
        self.newLine = QtWidgets.QLineEdit()
        self.numberLine = QtWidgets.QLineEdit()
        self.paddingLine = QtWidgets.QLineEdit()
        
        self.prefixBtn = QtWidgets.QPushButton("prefix")
        self.suffixBtn = QtWidgets.QPushButton("suffix")
        self.searchReplaceBtn = QtWidgets.QPushButton("search replace")
        self.renamingBtn = QtWidgets.QPushButton("renaming")

    def create_layouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        
        origLineLayout = QtWidgets.QFormLayout()
        origLineLayout.addRow("orig", self.origLine)

        newLineLayout = QtWidgets.QFormLayout()
        newLineLayout.addRow("new", self.newLine)

        topLineLayout = QtWidgets.QHBoxLayout()
        topLineLayout.addLayout(origLineLayout)
        topLineLayout.addLayout(newLineLayout)
        mainLayout.addLayout(topLineLayout)

        topBtnLayout = QtWidgets.QHBoxLayout()
        topBtnLayout.addWidget(self.prefixBtn)
        topBtnLayout.addWidget(self.suffixBtn)
        topBtnLayout.addWidget(self.searchReplaceBtn)
        mainLayout.addLayout(topBtnLayout)

        paddingLineLayout = QtWidgets.QFormLayout()
        paddingLineLayout.addRow("padding", self.paddingLine)

        numberLineLayout = QtWidgets.QFormLayout()
        numberLineLayout.addRow("number", self.numberLine)

        bottomLineLayout = QtWidgets.QHBoxLayout()
        bottomLineLayout.addLayout(numberLineLayout)
        bottomLineLayout.addLayout(paddingLineLayout)
        mainLayout.addLayout(bottomLineLayout)

        mainLayout.addWidget(self.renamingBtn)
        
    def create_connections(self):
        self.prefixBtn.clicked.connect(self.prefix)
        self.suffixBtn.clicked.connect(self.suffix)
        self.searchReplaceBtn.clicked.connect(self.search_replace)
        self.renamingBtn.clicked.connect(self.renaming)

    def prefix(self):
        with UndoWith():
            self.na.set_value(new=self.newLine.text(), selection=mc.ls(sl=1))
            self.na.prefix()

    def suffix(self):
        with UndoWith():
            self.na.set_value(new=self.newLine.text(), selection=mc.ls(sl=1))
            self.na.suffix()

    def search_replace(self):
        with UndoWith():
            if self.origLine.text() == "":
                return
            self.na.set_value(orig=self.origLine.text(), new=self.newLine.text()
                                , selection=mc.ls(sl=1))
            self.na.search_replace()

    def renaming(self):
        with UndoWith():
            try:
                int(self.numberLine.text())
                int(self.paddingLine.text())
            except:
                mc.warning("number and padding need int type") 
                return
            if self.newLine.text() == "":
                return
            elif int(self.numberLine.text()) < 0:
                mc.warning("number > 0") 
                return
            elif int(self.paddingLine.text()) < 0:
                mc.warning("padding > 0") 
                return
            self.na.set_value(new=self.newLine.text(), number=self.numberLine.text()
                                , padding=self.paddingLine.text(), selection=mc.ls(sl=1))
            self.na.renaming()

    @classmethod
    def display(cls):
        with UndoWith():    
            if mc.window(NamingUI.UINAME, query=True, exists=True):
                mc.deleteUI(NamingUI.UINAME)
            ui = NamingUI()
            ui.show()

if __name__ == "__main__":
    NamingUI.display()