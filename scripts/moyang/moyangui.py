# -*-coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from mworkspacecontrol import MWorkspaceControl

import pymel.core as pm
import json
import os


class Moyang(QtWidgets.QMainWindow):

    ui_instance = None

    @classmethod
    def display(cls):
        if cls.ui_instance:
            cls.ui_instance.show_workspace_control()
        else:
            cls.ui_instance = cls()

    @classmethod
    def get_workspace_control_name(cls):
        return '{0}WorkspaceControl'.format(cls.__name__)

    @classmethod
    def get_ui_script(cls):
        ui_script = "from {0} import {1}\n{1}.display()".format(cls.__module__, cls.__name__)
        return ui_script
    
    def create_workspace_control(self):
        self.workspace_control_instance = MWorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.__class__.__name__, self, ui_script=self.get_ui_script())

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)

    def __init__(self):
        super(Moyang, self).__init__()

        self.create_widgets()
        self.create_connections()
        self.create_workspace_control()

    def create_widgets(self):
        self.options_dialog = QtWidgets.QDialog()
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "main.ui"), self)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "options.ui"), self.options_dialog)
        self.dockWidget.hide()
    
    def create_connections(self):
        self.dock_vis_btn.toggled.connect(self.dock_widget_visibility)
        self.option_btn.clicked.connect(self.options_window)

    def dock_widget_visibility(self):
        if self.dock_vis_btn.isChecked():
            self.dockWidget.show()
        else:
            self.dockWidget.hide()
        
    def options_window(self):
        self.options_dialog.exec_()

    def plus_translate(self, attr):
        print attr
    def plus_rotate(self, attr):
        print attr
    def plus_scale(self, attr):
        print attr
    
    def minus_translate(self, attr):
        print attr
    def minus_rotate(self, attr):
        print attr
    def minus_scale(self, attr):
        print attr
    
    def lock_attr(self, attr):
        print attr
    
    def hide_attr(self, attr):
        print attr