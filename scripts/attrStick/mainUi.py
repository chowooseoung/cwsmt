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

        self.attrCtrl = ac.AttrControl()

        self.actions()
        self.setupUi()
        self.connections()

    def setupUi(self):
        self.setObjectName(AttrStickUI.UINAME)
        self.setWindowTitle(AttrStickUI.UINAME)
        self.setFixedWidth(450)

        self.daTree = MyTreeWidget()
        self.daTree.setHeaderLabel("transform attr")
        self.daTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))
        self.daTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.daTree.customContextMenuRequested.connect(lambda x, y=self.daTree, z=self.refreshAction :self.show_context_menu(x, y, z))
        
        self.kaTree = MyTreeWidget()
        self.kaTree.setHeaderLabel("userDefine, keyable")
        self.kaTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))
        self.kaTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.kaTree.customContextMenuRequested.connect(lambda x, y=self.kaTree, z=self.refreshAction:self.show_context_menu(x, y, z))

        self.udTree = MyTreeWidget()
        self.udTree.setHeaderLabel("userDefined")
        self.udTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))
        self.udTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.udTree.customContextMenuRequested.connect(lambda x, y=self.udTree, z=self.refreshAction :self.show_context_menu(x, y, z))

        self.upBtn = QtWidgets.QPushButton("up")
        self.upBtn.setFixedWidth(60)
        self.downBtn = QtWidgets.QPushButton("down")
        self.downBtn.setFixedWidth(60)

        self.lnLabel = QtWidgets.QLabel("ln :")
        self.lnLine = QtWidgets.QLineEdit()
        self.typeLabel = QtWidgets.QLabel("type :")
        self.typeLine = QtWidgets.QLineEdit()
        completer = QtWidgets.QCompleter()
        QtGui.QStringListModel(["bool", ])
        
        self.typeLine.setCompleter(completer)

        self.keyableCheck = QtWidgets.QCheckBox("keyable")
        self.keyableCheck.setChecked(True)
        self.lockCheck = QtWidgets.QCheckBox("lock")

        self.hideBtn = QtWidgets.QPushButton("H")
        self.hideBtn.setFixedWidth(25)
        self.unHideBtn = QtWidgets.QPushButton("UH")
        self.unHideBtn.setFixedWidth(25)
        self.lockBtn = QtWidgets.QPushButton("L")
        self.lockBtn.setFixedWidth(25)
        self.unLockBtn = QtWidgets.QPushButton("UL")
        self.unLockBtn.setFixedWidth(25)

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
        keyLayout.addWidget(self.kaTree)
        keyLayout.addLayout(upDownLayout)
        udLayout = QtWidgets.QVBoxLayout()
        udLayout.addWidget(self.udTree)
        lockHideLayout = QtWidgets.QHBoxLayout()
        lockHideLayout.addWidget(self.hideBtn)
        lockHideLayout.addWidget(self.unHideBtn)
        lockHideLayout.addWidget(self.lockBtn)
        lockHideLayout.addWidget(self.unLockBtn)
        udLayout.addLayout(lockHideLayout)

        viewLayout.addWidget(self.daTree)
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

    def connections(self):
        self.upBtn.clicked.connect(self.refresh_tree)
        self.addBtn.clicked.connect(self.add_attr_btn)
        self.hideBtn.clicked.connect(self.hide_btn)
        self.lockBtn.clicked.connect(self.lock_btn)

        self.refreshAction.triggered.connect(self.refresh_tree)

    def actions(self):
        self.refreshAction = QtWidgets.QAction("refresh")

    def show_context_menu(self, point, widget, action):
        context_menu = QtWidgets.QMenu()
        context_menu.addAction(action)

        context_menu.exec_(widget.mapToGlobal(point))

    def refresh_tree(self):
        sel = pm.ls(selection=True)
        self.daTree.clear()
        self.kaTree.clear()
        self.udTree.clear()
        if sel == []:
            return
        dfList, kaList, udList = self.attrCtrl.get_attr_list(sel[0])
        for i in dfList:
            item = self.create_item(i)  
            self.daTree.addTopLevelItem(item)

        for i in kaList:
            item = self.create_item(i)  
            self.kaTree.addTopLevelItem(item)
        
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
    
    def up_btn(self):
        pass
    def down_btn(self):
        pass
    def hide_btn(self):
        with UndoWith():
            at = []
            dtItem = self.daTree.selectedItems()
            if len(dtItem):
                for i in dtItem:
                    at.append(i.text(0))
                    check = 0
            kaItem = self.kaTree.selectedItems()
            if len(kaItem):
                for i in kaItem:
                    at.append(i.text(0))
                    check = 1
            udItem = self.udTree.selectedItems()
            if len(udItem):
                for i in udItem:
                    at.append(i.text(0))
                    check = 2
            sel = pm.ls(sl=1)
            for i in sel:
                for x in at:
                    attr = pm.ls("{0}.{1}".format(i, x))[0]
                    try:
                        attr.getChildren()
                    except:
                        if self.keyableCheck.isChecked():
                            attr.setKeyable(True)
                        else:
                            attr.setKeyable(False)
        self.refresh_tree()
        if check == 0:
            print self.daTree.model().checkIndex()
            # pprint.pprint( dir(self.daTree.model()))
            # self.daTree.setCurrentItem(dtItem[0])
        elif check == 1:
            self.kaTree.selectedItems(at)
        elif check == 2:
            self.udTree.selectedItems(at)
    def lock_btn(self):
        with UndoWith():
            at = []
            check = []
            if len(self.daTree.selectedItems()):
                for i in self.daTree.selectedItems():
                    at.append(i.text(0))
                    check.append(0)
            if len(self.kaTree.selectedItems()):
                for i in self.kaTree.selectedItems():
                    at.append(i.text(0))
                    check.append(1)
            if len(self.udTree.selectedItems()):
                for i in self.udTree.selectedItems():
                    at.append(i.text(0))
                    check.append(2)
            sel = pm.ls(sl=1)
            for i in sel:
                for x in at:
                    attr = pm.ls("{0}.{1}".format(i, x))[0]
                    try:
                        attr.getChildren()
                    except:
                        if self.lockCheck.isChecked():
                            attr.setLocked(True)
                        else:
                            attr.setLocked(False)
        self.refresh_tree()
                
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