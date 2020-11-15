# -*-coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from mworkspacecontrol import MWorkspaceControl

import pymel.core as pm
import json
import os


class Moyang(QtWidgets.QMainWindow):

    ui_instance = None
    __colors = dict()
    __options = dict()

    @property
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c
    
    @property
    def options(self):
        return self.__options
    
    @options.setter
    def options(self, o):
        self.__options = o

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
        self.load_options()
        self.save_options()
        self.create_workspace_control()

    def create_widgets(self):
        self.options_dialog = QtWidgets.QDialog()
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "main.ui"), self)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "options.ui"), self.options_dialog)
        self.dockWidget.hide()
    
    def create_connections(self):
        self.dock_vis_btn.toggled.connect(self.dock_widget_visibility)
        self.option_btn.clicked.connect(self.options_window)
        self.dockWidget.topLevelChanged.connect(self.dock_widget_float)
        self.dockWidget.visibilityChanged.connect(self.dock_widget_hide)
        self.options_dialog.accepted.connect(self.edit_options)
        self.custom_color_btn.clicked.connect(self.set_custom_color)
        self.custom_color_btn.installEventFilter(self)

    def dock_widget_visibility(self):
        if self.dock_vis_btn.isChecked():
            self.dockWidget.show()
            if self.dockWidget.isWindow():
                self.moyang_widget.show() 
        else:
            self.dockWidget.hide()
    
    def dock_widget_float(self, state):
        if state:
            self.moyang_widget.show()
        else:
            self.moyang_widget.hide()
    
    def dock_widget_hide(self, state):
        if state:
            self.dock_vis_btn.setChecked(True)
            self.moyang_widget.hide()
        else:
            self.dock_vis_btn.setChecked(False)
            self.moyang_widget.show()

    def edit_options(self):
        if self.options_dialog.world_radio.isChecked(): self.options["Space"] = "world"
        if self.options_dialog.object_radio.isChecked(): self.options["Space"] = "object"
        self.options["TranslateSnap"] = float(self.options_dialog.t_snap_line.text())
        self.options["RotateSnap"] = float(self.options_dialog.r_snap_line.text())
        self.options["ScaleSnap"] = float(self.options_dialog.s_snap_line.text())
        rows = self.options_dialog.mirror_table.rowCount()
        temp = dict()
        for row in range(rows):
            left = self.options_dialog.mirror_table.item(row, 0)
            right = self.options_dialog.mirror_table.item(row, 1)
            if left and right:
                temp[left.data(QtCore.Qt.DisplayRole)] = right.data(QtCore.Qt.DisplayRole)
        self.options["MirrorFilter"] = temp
        self.save_options()

    def load_options(self):
        option_path = os.path.join(os.path.dirname(__file__), "json", "options.json")
        if not os.path.exists(option_path):
            os.makedirs(os.path.dirname(option_path))
            with open(option_path, "w") as f:
                json.dump(dict(), f, indent=4)
        with open(option_path, "r") as f:
            self.options = json.load(f)
        
        if not self.options:
            self.options["color1"] = (0, 0, 30)
            self.options["color2"] = (255, 0, 0)
            self.options["color3"] = (0, 255, 0)
            self.options["color4"] = (0, 0, 205)
            self.options["color5"] = (255, 255, 0)
            self.options["color6"] = (148, 0, 211)
            self.options["color7"] = (255, 69, 0)
            self.options["color8"] = (53, 19, 7)
            self.options["color9"] = (255, 20, 147)
            self.options["color10"] = (50, 205, 50)
            self.options["color11"] = (5, 200, 200)
            self.options["color12"] = (255, 255, 102)
            self.options["color13"] = (238, 130, 238)
            self.options["color14"] = (112, 128, 144)

            self.options["Space"] = "object"
            self.options["TranslateSnap"] = 25
            self.options["RotateSnap"] = 15
            self.options["ScaleSnap"] = 0.1
            self.options["MirrorFilter"] = {"L*":"R*"}

        self.color1_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color1"]))
        self.color2_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color2"]))
        self.color3_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color3"]))
        self.color4_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color4"]))
        self.color5_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color5"]))
        self.color6_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color6"]))
        self.color7_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color7"]))
        self.color8_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color8"]))
        self.color9_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color9"]))
        self.color10_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color10"]))
        self.color11_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color11"]))
        self.color12_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color12"]))
        self.color13_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color13"]))
        self.color14_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*self.options["color14"]))
        self.color1_btn.setProperty("color", self.options["color1"])
        self.color2_btn.setProperty("color", self.options["color2"])
        self.color3_btn.setProperty("color", self.options["color3"])
        self.color4_btn.setProperty("color", self.options["color4"])
        self.color5_btn.setProperty("color", self.options["color5"])
        self.color6_btn.setProperty("color", self.options["color6"])
        self.color7_btn.setProperty("color", self.options["color7"])
        self.color8_btn.setProperty("color", self.options["color8"])
        self.color9_btn.setProperty("color", self.options["color9"])
        self.color10_btn.setProperty("color", self.options["color10"])
        self.color11_btn.setProperty("color", self.options["color11"])
        self.color12_btn.setProperty("color", self.options["color12"])
        self.color13_btn.setProperty("color", self.options["color13"])
        self.color14_btn.setProperty("color", self.options["color14"])

        if self.options["Space"] == "world":
            self.options_dialog.world_radio.setChecked(True)
        else:
            self.options_dialog.object_radio.setChecked(True)
        self.options_dialog.t_snap_line.setText(str(self.options["TranslateSnap"]))
        self.options_dialog.r_snap_line.setText(str(self.options["RotateSnap"]))
        self.options_dialog.s_snap_line.setText(str(self.options["ScaleSnap"]))
        self.options_dialog.mirror_table.clearContents()
        for index, key in enumerate(self.options["MirrorFilter"].keys()):
            left_item = QtWidgets.QTableWidgetItem(key)
            right_item = QtWidgets.QTableWidgetItem(self.options["MirrorFilter"][key])
            self.options_dialog.mirror_table.setItem(index, 0, left_item)
            self.options_dialog.mirror_table.setItem(index, 1, right_item)

    def save_options(self):
        option_path = os.path.join(os.path.dirname(__file__), "json", "options.json")
        with open(option_path, "w") as f:
            json.dump(self.options, f, indent=4)
        self.load_options()

    def options_window(self):
        self.load_options()
        self.options_dialog.exec_()

    def set_custom_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            print "red: {0}, green: {1}, blue: {2}".format(*color.getRgb())
            self.custom_color_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*color.getRgb()))
            self.custom_color_btn.setProperty("color", color.getRgb())

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
    
    def eventFilter(self, obj, event):
        if (obj == self.custom_color_btn) and (event.type() == QtCore.QEvent.MouseButtonRelease):
            wid = QtWidgets.QApplication.instance().widgetAt(event.pos())
            color = obj.property("color")
            p = event.pos() # relative to widget
            gp = self.mapToGlobal(p) # relative to screen
            rw = self.window().mapFromGlobal(gp) # relative to window
            print p, gp, rw
            print (obj != wid)
            print color
            print self.childAt(p).objectName()
            print 
            if wid:
                if (obj != wid) and color and wid.property("color"):
                    wid.setProperty("color", (color[0], color[1], color[2]))
                    wid.setStyleSheet("background-color:rgb({0},{1},{2})".format(color[0], color[1], color[2]))
        return super(Moyang, self).eventFilter(obj, event)