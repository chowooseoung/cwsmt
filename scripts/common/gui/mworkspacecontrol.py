#######################################################
# using code : testcode/exampleui.py
#######################################################

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import getCppPointer

import maya.OpenMayaUI as omui
import pymel.core as pm


class MWorkspaceControl(object):

    def __init__(self, name):
        self.name = name
        self.widget = None

    def create(self, label, widget, ui_script=None, vis=True):

        pm.workspaceControl(self.name, label=label, visible=False)

        if ui_script:
            pm.workspaceControl(self.name, e=True, uiScript=ui_script, visible=False)

        self.add_widget_to_layout(widget)
        if vis == True:
            self.set_visible(True)

    def restore(self, widget):
        self.add_widget_to_layout(widget)

    def add_widget_to_layout(self, widget):
        if widget:
            self.widget = widget
            self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)

            workspace_control_ptr = long(omui.MQtUtil.findControl(self.name))
            widget_ptr = long(getCppPointer(self.widget)[0])

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)

    def exists(self):
        return pm.workspaceControl(self.name, q=True, exists=True)

    def is_visible(self):
        return pm.workspaceControl(self.name, q=True, visible=True)

    def set_visible(self, visible):
        if visible:
            pm.workspaceControl(self.name, e=True, restore=True)
        else:
            pm.workspaceControl(self.name, e=True, visible=False)

    def set_label(self, label):
        pm.workspaceControl(self.name, e=True, label=label)

    def is_floating(self):
        return pm.workspaceControl(self.name, q=True, floating=True)

    def is_collapsed(self):
        return pm.workspaceControl(self.name, q=True, collapse=True)


class CustomUI(object):

    uiInstance = None


    @classmethod
    def display(cls):
        if cls.uiInstance:
            cls.uiInstance.show_workspace_control()
        else:
            cls.uiInstance = cls()

    @classmethod
    def get_workspace_control_name(cls):
        return '{0}WorkspaceControl'.format(cls.__name__)

    @classmethod
    def get_ui_script(cls):
        ui_script = "from {0} import {1}\n{1}.display()".format(cls.__module__, cls.__name__)
        return ui_script


    def __init__(self):
        super(CustomUI, self).__init__()

        self.setObjectName(self.__class__.__name__)

        self.create_workspace_control()

    def create_workspace_control(self):
        self.workspace_control_instance = MWorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.__class__.windowTitle, self, ui_script=self.get_ui_script())

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)


