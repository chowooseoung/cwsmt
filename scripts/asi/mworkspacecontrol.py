from Qt import QtWidgets, QtCore, QtGui
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
            pm.workspaceControl(self.name, edit=True, uiScript=ui_script, visible=False)

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
        return pm.workspaceControl(self.name, query=True, exists=True)

    def is_visible(self):
        return pm.workspaceControl(self.name, query=True, visible=True)

    def set_visible(self, visible):
        if visible:
            pm.workspaceControl(self.name, edit=True, restore=True)
        else:
            pm.workspaceControl(self.name, edit=True, visible=False)

    def set_label(self, label):
        pm.workspaceControl(self.name, edit=True, label=label)

    def is_floating(self):
        return pm.workspaceControl(self.name, query=True, floating=True)

    def is_collapsed(self):
        return pm.workspaceControl(self.name, query=True, collapse=True)