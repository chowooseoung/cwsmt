import sys
sys.path.append("D:\maya\scripts")

from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
from common.gui.uiloader import UiLoader
from common.gui.mworkspacecontrol import MWorkspaceControl
from shelfDelegate import ShelfDelegate, ShelfModel, ShelfItem

import glob
import json
import os


class RoomUI(QtWidgets.QDialog):

    windowTitle = 'Room' 
    uiFile = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'))

    preferenceJsonFile = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, '.room', 'preference.json'))

    uiInstance = None

    # maya workspace method # 
    @classmethod
    def display(cls, host):
        if cls.uiInstance:
            cls.uiInstance.show_workspace_control()
        else:
            cls.uiInstance = cls(host)

    @classmethod
    def get_workspace_control_name(cls):
        return "{0}WorkspaceControl".format(cls.__name__)

    @classmethod
    def get_ui_script(cls):
        ui_script = "from {0} import {1}\n{1}.display('maya')".format(cls.__module__, cls.__name__)
        return ui_script

    def create_workspace_control(self):
        self.workspace_control_instance = MWorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.__class__.windowTitle, self, ui_script=self.get_ui_script())

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True) ## 

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, h):
        self.__host = h

    @property
    def prefInitJson(self):
        path = [[os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'maya')),
                os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'maya', 'scripts')),
                os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'maya', 'plug-ins'))]]
        return self.create_pref_json(['maya'], path)

    def create_pref_json(self, tools, path):
        json = {}
        json['tools'] = tools
        for i in range(len(tools)):
            json[tools[i]] = {'shelfPath' : path[i][0],
                            'scriptsPath' : path[i][1],
                            'pluginsPath' : path[i][2]}
        return json

    def __init__(self, host):
        super(RoomUI, self).__init__()
        UiLoader().loadUi(uifile=self.uiFile, baseinstance=self)

        self.setObjectName(self.__class__.__name__)

        self.create_workspace_control()

        self.shelfModel = ShelfModel()
        self.listView.setItemDelegate(ShelfDelegate())
        self.listView.setModel(self.shelfModel)

        self.host = host
        if not os.path.exists(RoomUI.preferenceJsonFile):
            self.dump_json(self.prefInitJson, RoomUI.preferenceJsonFile)
        self.preferenceJson = self.load_json(RoomUI.preferenceJsonFile)

        if self.host == 'maya':
            import pymel.core as pm
            userShelfDir = pm.system.internalVar(userShelfDir=True)
            mayaJsonFIle = os.path.normpath(os.path.join(userShelfDir, 'room.mayaShelf.json'))
            if os.path.exists(mayaJsonFIle):
                mayaJson = self.load_json(mayaJsonFIle)
                if mayaJson.has_key('shelf'):
                    self.shelf = mayaJson['shelf']
                else:
                    self.shelf = None
            else:
                mayaJson = {}
                self.dump_json({}, mayaJsonFIle)
                self.shelf = None
            self.userJson = mayaJson

        self.init_listview()

    def init_listview(self):
        if not self.shelf:
            shelfList = glob.glob(os.path.normpath(os.path.join(self.preferenceJson[self.host]['shelfPath'], '*.json')))
            for i in range(len(shelfList)):
                json = self.load_json(shelfList[i])
                btn = QtWidgets.QToolButton()
                btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
                btn.setIcon(QtGui.QIcon(json['icon']))
                btn.setText(shelfList[i])
                btn.setCheckable(True)
                btn.setChecked(False)
                btn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                item = ShelfItem(name=shelfList[i], runCode=None, toolTip=None, icon=None, label=shelfList[i], widget=btn)
                self.shelfModel.appendRow(item)
            print('init_listview')
            return
        else:
            pass

    def load_json(self, jsonFile):
        with open(jsonFile, 'r') as f:
            r = json.load(f)
        return r

    def dump_json(self, data, jsonFile):
        with open(jsonFile, 'w') as f:
            json.dump(data, f, indent=4)

    def showEvent(self, e):
        super(RoomUI, self).showEvent(e)

        print('showEvent')
    
    def closeEvent(self, e):
        super(RoomUI, self).closeEvent(e)

        print('closeEvent')

    def hideEvent(self, e):
        super(RoomUI, self).hideEvent(e)

        print('hideEvent')


if __name__ == "__main__":
    """ Run the application. """
    from PySide2.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                                   QAbstractItemView)
    app = QApplication(sys.argv)

    test3ui = RoomUI('maya')
    test3ui.show()

    sys.exit(app.exec_())
