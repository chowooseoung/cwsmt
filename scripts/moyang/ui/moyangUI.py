#-*- coding:utf-8 -*-

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.mel as mel
import maya.OpenMayaUI as omui  

import sys
import os
import pprint
import inspect
import importlib

import moyang.core.moyang as mo
reload(mo)


def maya_main_window():
    
    mayaMainPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaMainPtr), QtWidgets.QWidget)
    
class undoWith():

    def __enter__(self):
        mc.undoInfo(ock=1)
    
    def __exit__(self, *args):
        mc.undoInfo(cck=1)

class DeleteWidget(QtWidgets.QDialog):

    def __init__(self, parent=None, name=None):
        super(DeleteWidget, self).__init__(parent=parent)
        self.name = name
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.confirmLabel = QtWidgets.QLabel("렬루 '{0}'를 삭제하시겠습니까?".format(self.name))
        self.okBtn = QtWidgets.QPushButton("ok")
        self.cancelBtn = QtWidgets.QPushButton("cancel")

    def create_layouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.confirmLabel)

        okCancelLayout = QtWidgets.QGridLayout()
        mainLayout.addLayout(okCancelLayout)

        okCancelLayout.addWidget(self.okBtn, 0, 1)
        okCancelLayout.addWidget(self.cancelBtn, 0, 2)

    def create_connections(self):
        self.okBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)


class MoYangUI(QtWidgets.QDialog):
    
    UINAME = "moyangUI"
    initialDirName = "collection"
    
    info = {}
    
    def __init__(self, parent=maya_main_window()):
        super(MoYangUI, self).__init__(parent)
        
        self.setObjectName(MoYangUI.UINAME)
        self.setWindowTitle("MoYang")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setFixedWidth(303)
        self.setMinimumHeight(300)
        
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        self.init_directory()
        self.search_directory()
        
        self.setStyleSheet("QToolTip {\
                                      font-size:9pt;\
                                      color:black; padding:2px;\
                                      border-width:2px;\
                                      border-style:solid;\
                                      background-color: rgb(135, 255, 255);\
                                      border: 2px solid rgb(5, 180, 180);\
                                      overflow:hidden;}");
    def create_actions(self):
        self.moyangLoadAction = QtWidgets.QAction("Load", self)

    def create_widgets(self):
        '''
        print "TODO: widgets"
        
        args: None
        
        return: None
        '''
        
        self.directoryBtn = QtWidgets.QPushButton("repo")
        self.directoryBtn.setFlat(1)
        self.directoryBtn.setFixedSize(285,20)
        
        self.txtLE = QtWidgets.QLineEdit()
        self.saveBtn = QtWidgets.QPushButton("save")
        size = 64
        self.shapeListWidget = QtWidgets.QListWidget()
        self.shapeListWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.shapeListWidget.setDragEnabled(0)
        self.shapeListWidget.setIconSize(QtCore.QSize(size, size))
        self.shapeListWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.shapeListWidget.setGridSize(QtCore.QSize(size+4, size+12))
        self.shapeListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shapeListWidget.customContextMenuRequested.connect(self.show_context_menu)
        
        self.customColorBtn = QtWidgets.QPushButton()
        self.customColorBtn.setFixedSize(57,57)
        
        self.defaultColor = (0,0,30)
        self.colorDefaultBtn = QtWidgets.QPushButton()
        self.colorDefaultBtn.setFixedSize(25,25)
        self.colorDefaultBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.defaultColor));
        
        self.redColor = (255, 0, 0)
        self.redBtn = QtWidgets.QPushButton()
        self.redBtn.setFixedSize(25,25)
        self.redBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.redColor));
        
        self.limeColor = (0, 255, 0)
        self.limeBtn = QtWidgets.QPushButton()
        self.limeBtn.setFixedSize(25,25)
        self.limeBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.limeColor))
        
        self.mediumblueColor = (0,0,205)
        self.mediumblueBtn = QtWidgets.QPushButton()
        self.mediumblueBtn.setFixedSize(25,25)
        self.mediumblueBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.mediumblueColor))
        
        self.yellowColor = (255, 255, 0)
        self.yellowBtn = QtWidgets.QPushButton()
        self.yellowBtn.setFixedSize(25,25)
        self.yellowBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.yellowColor))
        
        self.darkvioletColor = (148,0,211)
        self.darkvioletBtn = QtWidgets.QPushButton()
        self.darkvioletBtn.setFixedSize(25,25)
        self.darkvioletBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.darkvioletColor))
        
        self.orangeredColor = (255,69,0)
        self.orangeredBtn = QtWidgets.QPushButton()
        self.orangeredBtn.setFixedSize(25,25)
        self.orangeredBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.orangeredColor))
        
        self.brownColor  = (53, 19, 7)
        self.brownBtn = QtWidgets.QPushButton()
        self.brownBtn.setFixedSize(25,25)
        self.brownBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.brownColor ))
        
        self.deeppinkColor = (255,20,147)
        self.deeppinkBtn = QtWidgets.QPushButton()
        self.deeppinkBtn.setFixedSize(25,25)
        self.deeppinkBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.deeppinkColor))
        
        self.limegreenColor = (50, 205, 50)
        self.limegreenBtn = QtWidgets.QPushButton()
        self.limegreenBtn.setFixedSize(25,25)
        self.limegreenBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.limegreenColor))
        
        self.darkturquoiseColor = (5, 200, 200)
        self.darkturquoiseBtn = QtWidgets.QPushButton()
        self.darkturquoiseBtn.setFixedSize(25,25)
        self.darkturquoiseBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.darkturquoiseColor))
        
        self.lightYellow3Color = (255, 255, 102)
        self.lightYellow3Btn = QtWidgets.QPushButton()
        self.lightYellow3Btn.setFixedSize(25,25)
        self.lightYellow3Btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.lightYellow3Color))
        
        self.violetColor = (238,130,238)
        self.violetBtn = QtWidgets.QPushButton()
        self.violetBtn.setFixedSize(25,25)
        self.violetBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.violetColor))
        
        self.slategreyColor = (112, 128, 144)
        self.slategreyBtn = QtWidgets.QPushButton()
        self.slategreyBtn.setFixedSize(25,25)
        self.slategreyBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.slategreyColor))
        
        self.replaceBtn = QtWidgets.QPushButton("replace")
        self.mirrorBtn = QtWidgets.QPushButton("mirror")
        self.deleteBtn = QtWidgets.QPushButton("delete")
        
    def create_layouts(self):
        '''
        print "TODO: layouts"
        
        args: None
        
        return: None
        '''
        
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.directoryBtn)
        mainLayout.setContentsMargins(7,7,7,7)
        mainLayout.setSpacing(7)
        
        saveLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(saveLayout)
        
        saveLayout.addWidget(self.txtLE)
        saveLayout.addWidget(self.saveBtn)
        
        mainLayout.addWidget(self.shapeListWidget)
        
        colorLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(colorLayout)
        
        colorLayout.addWidget(self.customColorBtn)
        colorLayout.setContentsMargins(2,0,0,0)
        
        colorDivLayout = QtWidgets.QVBoxLayout()
        colorLayout.addLayout(colorDivLayout)
        
        colorUpLineLayout = QtWidgets.QHBoxLayout()
        colorDownLintLayout = QtWidgets.QHBoxLayout()
        colorDivLayout.addLayout(colorUpLineLayout)
        colorDivLayout.addLayout(colorDownLintLayout)
        
        colorUpLineLayout.addWidget(self.colorDefaultBtn)
        colorUpLineLayout.addWidget(self.redBtn)
        colorUpLineLayout.addWidget(self.limeBtn)
        colorUpLineLayout.addWidget(self.mediumblueBtn)
        colorUpLineLayout.addWidget(self.yellowBtn)
        colorUpLineLayout.addWidget(self.darkvioletBtn)
        colorUpLineLayout.addWidget(self.orangeredBtn)
        
        colorDownLintLayout.addWidget(self.brownBtn)
        colorDownLintLayout.addWidget(self.deeppinkBtn)
        colorDownLintLayout.addWidget(self.limegreenBtn)
        colorDownLintLayout.addWidget(self.darkturquoiseBtn)
        colorDownLintLayout.addWidget(self.lightYellow3Btn)
        colorDownLintLayout.addWidget(self.violetBtn)
        colorDownLintLayout.addWidget(self.slategreyBtn)
        
        colorLayout.addStretch()
        
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.setContentsMargins(2,0,2,0)
        mainLayout.addLayout(buttonLayout)
        
        buttonLayout.addWidget(self.replaceBtn)
        buttonLayout.addWidget(self.mirrorBtn)
        buttonLayout.addWidget(self.deleteBtn)
        
    def create_connections(self):
        '''
        print "TODO: connections"
        
        args: None
        
        return: None
        '''
        self.moyangLoadAction.triggered.connect(self.moyang_load)

        self.directoryBtn.clicked.connect(self.open_directory)
        self.saveBtn.clicked.connect(self.moyang_save)
        
        self.customColorBtn.clicked.connect(self.set_custom_color)
                
        self.colorDefaultBtn.clicked.connect(lambda:self.color_change(*self.defaultColor))
        self.redBtn.clicked.connect(lambda:self.color_change(*self.redColor))
        self.limeBtn.clicked.connect(lambda:self.color_change(*self.limeColor))
        self.mediumblueBtn.clicked.connect(lambda:self.color_change(*self.mediumblueColor))
        self.yellowBtn.clicked.connect(lambda:self.color_change(*self.yellowColor))
        self.darkvioletBtn.clicked.connect(lambda:self.color_change(*self.darkvioletColor))
        self.orangeredBtn.clicked.connect(lambda:self.color_change(*self.orangeredColor))
        
        self.brownBtn.clicked.connect(lambda:self.color_change(*self.brownColor))
        self.deeppinkBtn.clicked.connect(lambda:self.color_change(*self.deeppinkColor))
        self.limegreenBtn.clicked.connect(lambda:self.color_change(*self.limegreenColor))
        self.darkturquoiseBtn.clicked.connect(lambda:self.color_change(*self.darkturquoiseColor))
        self.lightYellow3Btn.clicked.connect(lambda:self.color_change(*self.lightYellow3Color))
        self.violetBtn.clicked.connect(lambda:self.color_change(*self.violetColor))
        self.slategreyBtn.clicked.connect(lambda:self.color_change(*self.slategreyColor))
        
        self.replaceBtn.clicked.connect(self.replace_con)
        self.mirrorBtn.clicked.connect(self.mirror_con)
        self.deleteBtn.clicked.connect(self.moyang_delete)
    
    def show_context_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.moyangLoadAction)

        context_menu.exec_(self.shapeListWidget.mapToGlobal(point))

    def init_directory(self):
        '''
        print "TODO: init directory"
        
        args: None
        
        return: None
        '''
        moPath = os.path.dirname(mo.__file__)
        collectionPath = QtCore.QDir.toNativeSeparators(os.path.join(os.path.normpath(os.path.join(moPath, os.pardir)), MoYangUI.initialDirName))
        print "collectionPath: {0}\n".format(collectionPath)
        if not os.path.isdir(collectionPath):
            os.mkdir(collectionPath)
        if not os.path.isfile(os.path.join(collectionPath, "__init__.py")):
            with open(os.path.join(collectionPath, "__init__.py"), "w") as f:
                f.write("")
        if collectionPath not in sys.path:
            sys.path.append(collectionPath)
        
        self.directoryBtn.setText(collectionPath)
        self.directoryBtn.setToolTip(self.directoryBtn.text())
        self.directoryBtn.setStyleSheet("QPushButton {color:rgb(255,255,255)}")
            
    def set_directory(self):
        '''
        print "TODO: directory set"
        
        args: None
        
        return: None
        '''
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "select folder", self.directoryBtn.text())
        
        if not path:
            self.directoryBtn.setText("you must confirm path")
            self.directoryBtn.setStyleSheet("QPushButton {color:rgb(%s,%s,%s)}" % self.yellowColor)
            self.directoryBtn.setToolTip(self.directoryBtn.text())
            self.search_directory()   
            return
            
        path = QtCore.QDir.toNativeSeparators(path)
        print "directory path: {0}".format(path)
        if not os.path.isdir(path):
            os.mkdir(path)
        if not os.path.isfile(os.path.join(path, "__init__.py")):
            with open(os.path.join(path, "__init__.py"), "w") as f:
                f.write("")
        if path not in sys.path:
            sys.path.append(path)
            
        self.directoryBtn.setText(path)
        self.directoryBtn.setStyleSheet("QPushButton {color:rgb(255,255,255)}")
        self.directoryBtn.setToolTip(self.directoryBtn.text())     
        self.search_directory()   
        
    def search_directory(self):
        '''
        print "TODO: search directory"
        
        args: None
        
        return: None
        '''
        MoYangUI.info = {}
        path = self.directoryBtn.text()
        
        self.shapeListWidget.clear()
        pylist = []
        sslist = []
        if not os.path.isdir(path):
            return
        for i in os.listdir(path):
            if i.endswith(".py"):
                if "_init_" not in i:
                    pylist.append(i)

        for i in range(len(pylist)):
            item = QtWidgets.QListWidgetItem(pylist[i].split(".")[0])
            self.shapeListWidget.addItem(item)
        
            pyPath = os.path.join(path, pylist[i])
            ssPath = os.path.join(path, "{0}.png".format(pylist[i].split(".")[0]))
            if not os.path.isfile(ssPath):
                ssPath = u""
            MoYangUI.info[pylist[i].split(".")[0]] = {"pyPath":pyPath, "ssPath":ssPath}
            
            if ssPath != "":
                icon = QtGui.QIcon(MoYangUI.info[pylist[i].split(".")[0]]["ssPath"])
                item.setIcon(icon)
            item.setToolTip(pprint.pformat(MoYangUI.info[pylist[i].split(".")[0]]))
        
        pprint.pprint(MoYangUI.info)
        
    def open_directory(self):
        '''
        print "TODO: open collection directory"
        
        args: None
        
        return: None
        '''
        print self.directoryBtn.text()
        path = self.directoryBtn.text()
        os.startfile(path)
        
    def moyang_save(self):
        '''
        print "TODO: controller save"
        '''

        with undoWith():
            selection = mc.ls(sl=1)
            if len(selection) != 1:
                return
            if mc.listRelatives(selection, s=1) == None:
                return
            if mc.nodeType(mc.listRelatives(selection, s=1)[0]) != "nurbsCurve":
                return

            path = self.directoryBtn.text()
            fileName = self.txtLE.text()

            pyTxt = mo.get_shape(selection[0], fileName)
            
            if fileName == "":
                return
                
            pyPath = os.path.join(path, "{0}.py".format(fileName))
            ssPath = os.path.join(path, "{0}.png".format(fileName))

            if os.path.isfile(pyPath):
                os.remove(pyPath)

            with open(pyPath, "w") as f:
                f.write(pyTxt)

            self.search_directory()
            
    def moyang_load(self):
        '''
        print "TODO: controller load"
        
        args: txt(module name)
        
        return: None
        '''
        with undoWith():
            if self.shapeListWidget.selectedItems() == []:
                return
            
            crv = self.shapeListWidget.selectedItems()[0].text()
            fileName = importlib.import_module(crv)
            reload(fileName)
            
            selection = mc.ls(sl=1)
            crvList = []
            if selection:
                for i in range(len(selection)):
                    crvList.append(fileName.create())
                    mc.xform(crvList[i], t=mc.xform(selection[i], q=1, t=1, ws=1), ws=1)
                    mc.xform(crvList[i], ro=mc.xform(selection[i], q=1, ro=1, ws=1), ws=1)
            else:
                crvList.append(fileName.create())
            print "Done"
            return crvList
            
    def moyang_delete(self):
        '''
        print "TODO: save file delete"
        '''
        if self.shapeListWidget.selectedItems() == []:
            return
        deleteWindow = DeleteWidget(parent=self, name=self.shapeListWidget.selectedItems()[0].text())
        
        if deleteWindow.exec_():        # cancelButton이 눌릴떄의 처리
            for i in self.shapeListWidget.selectedItems():
                path = QtCore.QDir.toNativeSeparators(os.path.join(self.directoryBtn.text(), "{0}.py".format(i.text())))
                if os.path.isfile(path):                
                    os.remove(path)
                path = QtCore.QDir.toNativeSeparators(os.path.join(self.directoryBtn.text(), "{0}.pyc".format(i.text())))
                if os.path.isfile(path):   
                    os.remove(path)
                path = QtCore.QDir.toNativeSeparators(os.path.join(self.directoryBtn.text(), "{0}.png".format(i.text())))
                if os.path.isfile(path):   
                    os.remove(path)
        else:
            return        # cancelButton이 눌릴떄의 처리

        self.search_directory()
        
    def replace_con(self):
        '''
        print "TODO: controller shape replace"
        '''
        with undoWith():
            selection = mc.ls(sl=1)
            if selection == []:
                return
            for i in selection:
                if mc.listRelatives(i, s=1) == None:
                    return

            crv = self.moyang_load()
            if not self.shapeListWidget.selectedItems():
                return
            mc.select(selection)
            mo.replace_con(newcon=crv)
            mc.delete(crv)
            print "Done"

    def mirror_con(self):
        '''
        print "TODO: mirror controller shape"

        L, R

        '''
        left = "L"
        right = "R"
        with undoWith():
            selection = mc.ls(sl=1)
            if selection == []:
                return
            for i in selection:
                if mc.listRelatives(i, s=1) == None:
                    return
            check = False
            for i in selection:
                if not (i.startswith(left) or i.startswith(right)):
                    print i
                    check = True
            if check == True:
                return
            
            for i in selection:
                if i.startswith(left):
                    name = i.replace(left, right, 1)
                elif i.startswith(right):
                    name = i.replace(right, left, 1)
                if not mc.objExists(name):
                    print "{0} is not exists".format(name)
                    check = True
            if check == True:
                return
            
            mo.mirror_con(scale=(-1, 1, 1), left=left, right=right)
            print "Done"
        
    def set_custom_color(self):
        '''
        print "TODO: custom color set color dialog"
        
        args: None
        
        return: None
        '''

        with undoWith():
            color = QtWidgets.QColorDialog.getColor()
            if color:
                print "red: {0}, green: {1}, blue: {2}".format(*color.getRgb())
                self.customColorBtn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*color.getRgb()))
                self.color_change(*color.getRgb())
            
    def color_change(self, *color):
        '''
        print "TODO: controller shape color change"
        print "r: {0}, g: {1}, b: {2}".format(*color)
        
        args: rgb color(tuple)
        
        return: None
        '''

        with undoWith():
            sel = mc.ls(sl=1)
            if sel == []:
                return
            for i in sel:
                selShape = mc.listRelatives(i, s=1)
                for x in selShape:
                    mc.setAttr("{0}.overrideEnabled".format(x), 1)
                    mc.setAttr("{0}.overrideRGBColors".format(x), 1)
                    if len(color) == 3:
                        r, g, b = color
                    elif len(color) > 3:    
                        r, g, b, _ = color
                    mc.setAttr("{0}.overrideColorRGB".format(x), r/255.0, g/255.0, b/255.0)
        
    def all_con_resize(self):
        print "TODO: all controller(*con) resize"

    @classmethod
    def display(cls):
        with undoWith():
            if mc.window(MoYangUI.UINAME, query=True, exists=True):
                mc.deleteUI(MoYangUI.UINAME)
            ui = MoYangUI()
            ui.show()

if __name__ == "__main__":
    sys.path.insert(0, "D:\maya\scripts")
    import moyang.ui.moyangUI as moui
    reload(moui)
    moui.MoYangUI.display()
    