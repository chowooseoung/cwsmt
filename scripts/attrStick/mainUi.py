from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import pymel.core as pm

import attrStick.attrCtrl as ac
reload(ac)

def maya_main_window():
    mainPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mainPtr), QtWidgets.QWidget)

class AttrStickUI(QtWidgets.QDialog):

    UINAME = "AttrStickUI"

    def __init__(self, parent=maya_main_window()):
        super(AttrStickUI, self).__init__(parent=parent)

        self.setObjectName(AttrStickUI.UINAME)
        self.setWindowTitle(AttrStickUI.UINAME)
        self.setFixedWidth(450)
        self.attrCtrl = ac.AttrControl()

        self.defaultTree = MyTreeWidget()
        self.defaultTree.setHeaderLabel("transform attr")
        self.defaultTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))
        
        self.keyTree = MyTreeWidget()
        self.keyTree.setHeaderLabel("userDefine, keyable")
        self.keyTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))

        self.udTree = MyTreeWidget()
        self.udTree.setHeaderLabel("userDefined")
        self.udTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))

        self.upBtn = QtWidgets.QPushButton("up")
        self.upBtn.setFixedWidth(60)
        self.downBtn = QtWidgets.QPushButton("down")
        self.downBtn.setFixedWidth(60)

        self.lnLabel = QtWidgets.QLabel("ln :")
        self.lnLine = QtWidgets.QLineEdit()
        self.typeLabel = QtWidgets.QLabel("type :")
        self.typeLine = QtWidgets.QLineEdit()

        self.keyableCheck = QtWidgets.QCheckBox("keyable")
        self.keyableCheck.setChecked(True)
        self.lockCheck = QtWidgets.QCheckBox("lock")

        self.hideBtn = QtWidgets.QPushButton("hide")
        self.hideBtn.setFixedWidth(60)
        self.lockBtn = QtWidgets.QPushButton("lock")
        self.lockBtn.setFixedWidth(60)

        self.hxvCheck = QtWidgets.QCheckBox("has max value")
        self.hnvCheck = QtWidgets.QCheckBox("has min value")

        self.maxLine = QtWidgets.QLineEdit()
        self.minLine = QtWidgets.QLineEdit()

        self.stringLine = QtWidgets.QLineEdit()

        self.addBtn = QtWidgets.QPushButton("add")
        self.addBtn.setFixedWidth(80)
        self.editBtn = QtWidgets.QPushButton("edit")
        self.editBtn.setFixedWidth(80)
        self.deleteBtn = QtWidgets.QPushButton("delete")
        self.deleteBtn.setFixedWidth(80)

        self.enumView = QtWidgets.QListWidget()
        self.enumView.setFixedSize(140, 150)

        mainLayout = QtWidgets.QVBoxLayout(self)

        viewLayout = QtWidgets.QHBoxLayout()

        upDownLayout = QtWidgets.QHBoxLayout()
        upDownLayout.addWidget(self.upBtn)
        upDownLayout.addWidget(self.downBtn)
        keyLayout = QtWidgets.QVBoxLayout()
        keyLayout.addWidget(self.keyTree)
        keyLayout.addLayout(upDownLayout)
        udLayout = QtWidgets.QVBoxLayout()
        udLayout.addWidget(self.udTree)
        lockHideLayout = QtWidgets.QHBoxLayout()
        lockHideLayout.addWidget(self.hideBtn)
        lockHideLayout.addWidget(self.lockBtn)
        udLayout.addLayout(lockHideLayout)

        viewLayout.addWidget(self.defaultTree)
        viewLayout.addLayout(keyLayout)
        viewLayout.addLayout(udLayout)
        mainLayout.addLayout(viewLayout)

        lnLayout = QtWidgets.QHBoxLayout()
        lnLayout.addWidget(self.lnLabel)
        lnLayout.addWidget(self.lnLine)
        lnLayout.addWidget(self.keyableCheck)
        typeLayout = QtWidgets.QHBoxLayout()
        typeLayout.addWidget(self.typeLabel)
        typeLayout.addWidget(self.typeLine)
        typeLayout.addWidget(self.lockCheck)

        hLayout = QtWidgets.QHBoxLayout()
        hasLayout = QtWidgets.QHBoxLayout()
        hasLayout.addWidget(self.hnvCheck)
        hasLayout.addWidget(self.hxvCheck)
        minMaxLayout = QtWidgets.QHBoxLayout()
        minMaxLayout.addWidget(self.minLine)
        minMaxLayout.addWidget(self.maxLine)

        attr1Layout = QtWidgets.QVBoxLayout()        
        attr1Layout.addLayout(lnLayout)
        attr1Layout.addLayout(typeLayout)
        attr1Layout.addLayout(hasLayout)
        attr1Layout.addLayout(minMaxLayout)
        attr1Layout.addWidget(self.stringLine)
        
        addEditLayout = QtWidgets.QHBoxLayout()
        addEditLayout.addWidget(self.addBtn)
        addEditLayout.addWidget(self.editBtn)
        addEditLayout.addWidget(self.deleteBtn)
        attr1Layout.addLayout(addEditLayout)

        hLayout.addLayout(attr1Layout)
        hLayout.addWidget(self.enumView)
        mainLayout.addLayout(hLayout)
        self.connections()

    def connections(self):
        self.upBtn.clicked.connect(self.refresh_tree)
        self.addBtn.clicked.connect(self.add_attr_btn)

    def refresh_tree(self):
        sel = pm.ls(selection=True)
        self.defaultTree.clear()
        self.keyTree.clear()
        self.udTree.clear()
        if sel == []:
            return
        dfList, kaList, udList = self.attrCtrl.get_attr_list(sel[0])
        for i in dfList:
            item = self.create_item(i)  
            self.defaultTree.addTopLevelItem(item)

        for i in kaList:
            item = self.create_item(i)  
            self.keyTree.addTopLevelItem(item)
        
        for i in udList:
            item = self.create_item(i, key=False)  
            self.udTree.addTopLevelItem(item)
        
    def create_item(self, attr, key=True):
        item = QtWidgets.QTreeWidgetItem([attr.longName()])
        self.add_children(item=item, attr=attr, key=key)

        return item

    def add_children(self, item, attr, key):
        try:
            children = attr.getChildren()
        except:
            children = False
        if children:
            for i in children:
                if key:
                    if i.isKeyable():
                        child_item = self.create_item(i)
                        item.addChild(child_item)
                else:
                    if not i.isKeyable():
                        child_item = self.create_item(i)
                        item.addChild(child_item)
    
    def add_attr_btn(self):
        with UndoWith():
            print 'a'
    def edit_attr_btn(self):
        with UndoWith():
            print 'b'
    def delete_attr_btn(self):
        with UndoWith():
            print 'c'

    @classmethod
    def display(cls):
        if pm.window(cls.UINAME, query=True, exists=True):
            pm.deleteUI(cls.UINAME)
        ui = AttrStickUI()
        ui.show()

class MyTreeWidget(QtWidgets.QTreeWidget):

    def __init__(self):
        super(MyTreeWidget, self).__init__()
    
    def focusOutEvent(self, e):
        self.clearSelection()
        QtWidgets.QTreeWidget.focusOutEvent(self, e)

class UndoWith():
    def __enter__(self):
        pm.undoInfo(ock=True)
    def __exit__(self, *args):
        pm.undoInfo(cck=True)

if __name__ == "__main__":
    AttrStickUI.display()