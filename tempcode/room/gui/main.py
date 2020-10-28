import maya.OpenMayaUI as omui
import pymel.core as pm

import glob
import json
import os

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from shiboken2 import wrapInstance
from common.gui.uiloader import UiLoader
from common.gui.mworkspacecontrol import MWorkspaceControl

from functools import partial
from collections import OrderedDict


class RoomUI(QtWidgets.QDialog):

    windowTitle = 'Room' 
    uiFile = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'))

    uiInstance = None

    ####################### maya workspace method #######################
    @classmethod
    def get_workspace_control_name(cls):
        return '{0}WorkspaceControl'.format(cls.__name__)

    @classmethod
    def get_ui_script(cls):
        ui_script = 'from {0} import {1}\n{1}.display()'.format(cls.__module__, cls.__name__)
        return ui_script

    def create_workspace_control(self):
        self.workspace_control_instance = MWorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.__class__.windowTitle, self, ui_script=self.get_ui_script(), vis=False)

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)
    #####################################################################

    ############################# diaplay ###############################
    @classmethod
    def display(cls):
        '''
        mode : popup, floating / type string
        '''
        if cls.uiInstance is None:
            cls.uiInstance = cls()
        elif bool(cls.uiInstance) & (cls.uiInstance.mode != None):
            cls.uiInstance.show_workspace_control()

    @classmethod
    def show_display(cls, m):
        if cls.uiInstance is None:
            cls.display()
        cls.uiInstance.mode = m
        json = cls.uiInstance.load_json(os.path.normpath(os.path.join(cls.uiInstance.preferencePath['.room'], 'preference.json')))
        if cls.uiInstance.mode != None:
            json['mode'] = cls.uiInstance.mode
        else:
            json['mode'] = None
        cls.uiInstance.dump_json(json, os.path.normpath(os.path.join(json['path']['.room'], 'preference.json')))
        cls.uiInstance.set_preferenceJson(json)
        cls.display()
    #####################################################################

    ############################# property #############################
    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, m):
        self.__mode = m

    @property
    def selectedRoom(self):
        return self.__selectedRoom
    
    @selectedRoom.setter
    def selectedRoom(self, r):
        self.__selectedRoom = r

    @property
    def preferencePath(self):
        return self.__preferencePath
    
    @preferencePath.setter
    def preferencePath(self, p):
        self.__preferencePath = p
    ####################################################################

    ############################## hotkey ############################### 
    def set_hotkey(self):
        mainWin = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        popupAction = QtWidgets.QAction(mainWin)
        floatingAction = QtWidgets.QAction(mainWin)

        def hotkey(mode):
            pm.evalDeferred('RoomUI.show_display("{0}")'.format(mode))

        popupAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Tab)) # ctrl tab
        popupAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        floatingAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Tab)) # ctrl shift tab
        floatingAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)

        popupAction.triggered.connect(partial(hotkey, mode='popup'))
        floatingAction.triggered.connect(partial(hotkey, mode='floating'))

        mainWin.addAction(popupAction)
        mainWin.addAction(floatingAction)
    #####################################################################
    
    ############################## json path ############################
    def init_preference(self):
        json = dict()
        json['path'] = dict()
        json['path']['.room'] = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, '.room')) # preference folder
        json['path']['team'] = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'room')) # team category folder
        json['path']['teamScripts'] = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'scripts')) # team scripts folder
        json['path']['teamPlugins'] = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'plug-ins')) # team plugins folder
        json['path']['user'] = os.path.normpath(os.path.join(pm.system.internalVar(userShelfDir=True), 'room')) # user category folder
        json['path']['userScripts'] = pm.system.internalVar(userScriptDir=True) # user scripts folder
        json['path']['userPlugins'] = os.path.normpath(os.path.join(pm.system.internalVar(userScriptDir=True), os.path.pardir, 'plug-ins')) # user plugins folder
        json['selectedRoom'] = [] # example : ['team', 'modeling', 0, 2 ,3] // json['team']['modeling'][0]['child'][2]['child'][3]['child']
        json['mode'] = None # None, popup, floating
        return json
    
    def set_preferenceJson(self, json):
        self.mode = json['mode']
        self.selectedRoom = json['selectedRoom']
        self.preferencePath = json['path']
    #####################################################################

    ############################ initialize ############################
    def room_init(self):
        initFolderPath = self.init_preference()['path']
        prefJsonFile = os.path.normpath(os.path.join(initFolderPath['.room'], 'preference.json'))
        if not os.path.exists(prefJsonFile):
            self.dump_json(self.init_preference(), prefJsonFile) # preference init json create
        self.set_preferenceJson(self.load_json(prefJsonFile)) # preference json load
        for i in self.preferencePath: # folder create   
            if not os.path.exists(self.preferencePath[i]):
                os.makedirs(self.preferencePath[i])
        userJsonFile = os.path.normpath(os.path.join(self.preferencePath['user'], 'user.json')) # default userJson
        if not os.path.exists(userJsonFile):
            self.dump_json(dict(), userJsonFile) # default userJson create

    def all_initialize(self):
        if os.path.exists(os.path.normpath(os.path.join(self.preferencePath['.room'], 'preference.json'))):
            os.remove(os.path.normpath(os.path.join(self.preferencePath['.room'], 'preference.json')))
        if os.path.exists(os.path.normpath(self.preferencePath['team'])):
            os.removedirs(os.path.normpath(self.preferencePath['team']))
        if os.path.exists(os.path.normpath(self.preferencePath['user'])):
            os.removedirs(os.path.normpath(self.preferencePath['user']))
        self.room_init()
    ####################################################################

    def __init__(self):
        super(RoomUI, self).__init__()

        self.setObjectName(self.__class__.__name__)
        QtCompat.loadUi(RoomUI.uiFile, self)
        self.create_workspace_control()
        self.set_hotkey()
        self.room_init()
        teamCategory = [x.split('.json')[0] for x in sorted(os.listdir(self.preferencePath['team']))]
        userCategory = [x.split('.json')[0] for x in sorted(os.listdir(self.preferencePath['user']))]
        self.itemDict = dict()
        self.itemDict['team'] = dict()
        self.itemDict['user'] = dict()
        for i in teamCategory:
            self.itemDict['team'][i] = self.load_json(os.path.normpath(os.path.join(self.preferencePath['team'], '{0}.json'.format(i))))
        for i in userCategory:
            self.itemDict['user'][i] = self.load_json(os.path.normpath(os.path.join(self.preferencePath['user'], '{0}.json'.format(i))))
        self.refresh_view()

        self.installEventFilter(self)

    ############################# add item #############################
    def new_item_data(self, name, typ, runCode, child, icon):
        item = dict()
        item['name'] = name # room name
        item['type'] = typ # python, mel, folder
        item['runCode'] = runCode # if python, mel else None
        item['child'] = child # if folder, child item type dict
        item['icon'] = icon # iconPath
        return item

    def add_item(self, item):
        excuteString = ''
        excuteString += 'self.itemDict'
        for i in range(len(self.selectedRoom)):
            if i < 2:
                excuteString += '["{0}"]'.format(self.selectedRoom[i])
            else:
                excuteString += '["{0}"]["child"]'.format(self.selectedRoom[i])
        num = len(excuteString)
        excuteString += '[{0}] = {1}'.format(num, item)
        exec(excuteString)
    
    def reorder_item_dict(self, itemDict):
        excuteString = ''
        excuteString += 'self.itemDict'
        for i in range(len(self.selectedRoom)):
            if i < 2:
                excuteString += '["{0}"]'.format(self.selectedRoom[i])
            else:
                excuteString += '["{0}"]["child"]'.format(self.selectedRoom[i])
        excuteString += ' = {1}'.format(itemDict)
        exec(excuteString)
    #####################################################################

    ############################### view ###############################
    def refresh_view(self):
        currentRoom = self.itemDict
        
        for i in range(len(self.selectedRoom)):
            if i < 2:
                if currentRoom.has_key(self.selectedRoom[i]):
                    currentRoom = currentRoom[self.selectedRoom[i]]
            elif i > 1:
                if currentRoom.has_key(self.selectedRoom[i]):
                    currentRoom = currentRoom[self.selectedRoom[i]]['child']
        
        if bool(currentRoom) is False:
            return
    ####################################################################
    
    ############################### json ###############################
    def load_json(self, jsonFile):
        with open(jsonFile, 'r') as f:
            r = json.load(f)
        return r

    def dump_json(self, data, jsonFile):
        with open(jsonFile, 'w') as f:
            json.dump(data, f, indent=4)
    ####################################################################

    ############################### event ###############################
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Type.WindowDeactivate:
            if self.mode == 'popup':
                self.workspace_control_instance.set_visible(False)
            return super(RoomUI, self).eventFilter(object, event)
        else:
            return super(RoomUI, self).eventFilter(object, event)
    #####################################################################
    
if __name__ == "__main__":
    ''' Run the application. '''

    from room.gui.main import RoomUI
    RoomUI.show_display(m=None)
