################################################################
# common/gui/workspacecontrol.py using code
################################################################
from PySide2 import QtWidgets, QtCore, QtGui
from common.gui.workspacecontrol import CustomUI
from common.gui.workspacecontrol import WorkspaceControl

import pymel.core as pm


class Test1UI(QtWidgets.QDialog, CustomUI):
    
    WINDOW_TITLE = "test ui"
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        
        btn = QtWidgets.QPushButton("testBtn")
        mainLayout = QtWidgets.QHBoxLayout(self)
        mainLayout.addWidget(btn)

        CustomUI.__init__(self)
        
    def showEvent(self, e):
        super(Test1UI, self).showEvent(e)

        print 'showEvent'
    
    def closeEvent(self, e):
        super(Test1UI, self).closeEvent(e)

        print 'closeEvent'
    
    def hideEvent(self, e):
        super(Test1UI, self).hideEvent(e)

        print 'hideEvent'


class Test2UI(QtWidgets.QDialog):

    WINDOW_TITLE = "Test2 UI"
    UI_NAME = "Test2UI"

    ui_instance = None


    @classmethod
    def display(cls):
        if cls.ui_instance:
            cls.ui_instance.show_workspace_control()
        else:
            cls.ui_instance = Test2UI()

    @classmethod
    def get_workspace_control_name(cls):
        return "{0}WorkspaceControl".format(cls.UI_NAME)

    @classmethod
    def get_ui_script(cls):
        ui_script = "from {0} import {1}\n{1}.display()".format(cls.__module__, cls.__name__)
        return ui_script


    def __init__(self):
        super(Test2UI, self).__init__()

        self.setObjectName(self.__class__.UI_NAME)
        self.setMinimumSize(200, 100)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.create_workspace_control()

    def create_widgets(self):
        self.apply_button = QtWidgets.QPushButton("Apply")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        main_layout.addWidget(self.apply_button)

    def create_connections(self):
        self.apply_button.clicked.connect(self.on_clicked)

    def create_workspace_control(self):
        self.workspace_control_instance = WorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.WINDOW_TITLE, self, ui_script=self.get_ui_script())

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)

    def on_clicked(self):
        print("Button Clicked")

    def showEvent(self, e):
        super(Test2UI, self).showEvent(e)

        if self.workspace_control_instance.is_floating():
            self.workspace_control_instance.set_label("Floating Window")
        else:
            self.workspace_control_instance.set_label("Docked Window")

        print 'showEvent'
            
    def closeEvent(self, e):
        super(Test2UI, self).closeEvent(e)

        print 'closeEvent'
    
    def hideEvent(self, e):
        super(Test2UI, self).hideEvent(e)

        print 'hideEvent'
