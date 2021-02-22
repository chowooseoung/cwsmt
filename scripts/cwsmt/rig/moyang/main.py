# -*-coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from mworkspacecontrol import MWorkspaceControl
from functools import partial

import pymel.core as pm
import numpy as np
import importlib
import json
import sys
import os
import re


class UndoInfo(object):
    
    def __enter__(self):
        pm.undoInfo(openChunk=True)
    
    def __exit__(self, *args):
        pm.undoInfo(closeChunk=True)

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
        self.reload()
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

        self.vis_btn.clicked.connect(partial(self.controller_controller, ["v"]))
        self.t_btn.clicked.connect(partial(self.controller_controller, ["tx", "ty", "tz"]))
        self.tx_btn.clicked.connect(partial(self.controller_controller, ["tx"]))
        self.ty_btn.clicked.connect(partial(self.controller_controller, ["ty"]))
        self.tz_btn.clicked.connect(partial(self.controller_controller, ["tz"]))
        self.r_btn.clicked.connect(partial(self.controller_controller, ["rx", "ry", "rz"]))
        self.rx_btn.clicked.connect(partial(self.controller_controller, ["rx"]))
        self.ry_btn.clicked.connect(partial(self.controller_controller, ["ry"]))
        self.rz_btn.clicked.connect(partial(self.controller_controller, ["rz"]))
        self.s_btn.clicked.connect(partial(self.controller_controller, ["sx", "sy", "sz"]))
        self.sx_btn.clicked.connect(partial(self.controller_controller, ["sx"]))
        self.sy_btn.clicked.connect(partial(self.controller_controller, ["sy"]))
        self.sz_btn.clicked.connect(partial(self.controller_controller, ["sz"]))

        self.save_btn.clicked.connect(self.save_controller)
        self.load_btn.clicked.connect(self.load_controller)
        self.delete_btn.clicked.connect(self.delete_controller)
        self.replace_btn.clicked.connect(self.replace_shape)
        self.mirror_btn.clicked.connect(self.mirror_shape)

        self.color1_btn.clicked.connect(partial(self.set_color, self.color1_btn))
        self.color2_btn.clicked.connect(partial(self.set_color, self.color2_btn))
        self.color3_btn.clicked.connect(partial(self.set_color, self.color3_btn))
        self.color4_btn.clicked.connect(partial(self.set_color, self.color4_btn))
        self.color5_btn.clicked.connect(partial(self.set_color, self.color5_btn))
        self.color6_btn.clicked.connect(partial(self.set_color, self.color6_btn))
        self.color7_btn.clicked.connect(partial(self.set_color, self.color7_btn))
        self.color8_btn.clicked.connect(partial(self.set_color, self.color8_btn))
        self.color9_btn.clicked.connect(partial(self.set_color, self.color9_btn))
        self.color10_btn.clicked.connect(partial(self.set_color, self.color10_btn))
        self.color11_btn.clicked.connect(partial(self.set_color, self.color11_btn))
        self.color12_btn.clicked.connect(partial(self.set_color, self.color12_btn))
        self.color13_btn.clicked.connect(partial(self.set_color, self.color13_btn))
        self.color14_btn.clicked.connect(partial(self.set_color, self.color14_btn))
        self.custom_color_btn.clicked.connect(self.set_custom_color)
        
        self.color1_btn.installEventFilter(self)
        self.color2_btn.installEventFilter(self)
        self.color3_btn.installEventFilter(self)
        self.color4_btn.installEventFilter(self)
        self.color5_btn.installEventFilter(self)
        self.color6_btn.installEventFilter(self)
        self.color7_btn.installEventFilter(self)
        self.color8_btn.installEventFilter(self)
        self.color9_btn.installEventFilter(self)
        self.color10_btn.installEventFilter(self)
        self.color11_btn.installEventFilter(self)
        self.color12_btn.installEventFilter(self)
        self.color13_btn.installEventFilter(self)
        self.color14_btn.installEventFilter(self)
        self.custom_color_btn.installEventFilter(self)

    def set_color(self, wid):
        with UndoInfo():
            selected_nodes = pm.ls(selection=True, type="transform")
            shapes = [ y for x in selected_nodes for y in x.getShapes() ]
            if wid.color:
                for shape in shapes:
                    shape.overrideEnabled.set(True)
                    shape.overrideRGBColors.set(True)
                    shape.overrideColorRGB.set((wid.color[0]/255.0, wid.color[1]/255.0, wid.color[2]/255.0))

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
        rows = self.options_dialog.mirror_table.rowCount()
        temp = dict()
        for row in range(rows):
            left = self.options_dialog.mirror_table.item(row, 0)
            right = self.options_dialog.mirror_table.item(row, 1)
            if left and right:
                if left.data(QtCore.Qt.DisplayRole) and right.data(QtCore.Qt.DisplayRole):
                    temp[left.data(QtCore.Qt.DisplayRole)] = right.data(QtCore.Qt.DisplayRole)
        self.options["MirrorFilter"] = temp
        self.save_options()

    def load_options(self):
        option_path = os.path.join(os.path.dirname(__file__), "json", "options.json")
        if not os.path.exists(os.path.dirname(option_path)):
            os.makedirs(os.path.dirname(option_path))
        if not os.path.exists(option_path):
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
            self.options["MirrorFilter"] = {"L":"R", "Left":"Right"}

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
        self.color1_btn.color = self.options["color1"]
        self.color2_btn.color = self.options["color2"]
        self.color3_btn.color = self.options["color3"]
        self.color4_btn.color = self.options["color4"]
        self.color5_btn.color = self.options["color5"]
        self.color6_btn.color = self.options["color6"]
        self.color7_btn.color = self.options["color7"]
        self.color8_btn.color = self.options["color8"]
        self.color9_btn.color = self.options["color9"]
        self.color10_btn.color = self.options["color10"]
        self.color11_btn.color = self.options["color11"]
        self.color12_btn.color = self.options["color12"]
        self.color13_btn.color = self.options["color13"]
        self.color14_btn.color = self.options["color14"]
        self.custom_color_btn.color = None
        self.custom_color_btn.setStyleSheet("")

        if self.options["Space"] == "world":
            self.world_radio.setChecked(True)
        else:
            self.object_radio.setChecked(True)
        self.t_snap_line.setText(str(self.options["TranslateSnap"]))
        self.r_snap_line.setText(str(self.options["RotateSnap"]))
        self.s_snap_line.setText(str(self.options["ScaleSnap"]))
        self.options_dialog.mirror_table.clearContents()
        for index, key in enumerate(self.options["MirrorFilter"].keys()):
            left_item = QtWidgets.QTableWidgetItem(key)
            right_item = QtWidgets.QTableWidgetItem(self.options["MirrorFilter"][key])
            self.options_dialog.mirror_table.setItem(index, 0, left_item)
            self.options_dialog.mirror_table.setItem(index, 1, right_item)

    def save_options(self):
        self.options["color1"] = self.color1_btn.color 
        self.options["color2"] = self.color2_btn.color 
        self.options["color3"] = self.color3_btn.color 
        self.options["color4"] = self.color4_btn.color 
        self.options["color5"] = self.color5_btn.color 
        self.options["color6"] = self.color6_btn.color 
        self.options["color7"] = self.color7_btn.color 
        self.options["color8"] = self.color8_btn.color 
        self.options["color9"] = self.color9_btn.color 
        self.options["color10"] = self.color10_btn.color
        self.options["color11"] = self.color11_btn.color
        self.options["color12"] = self.color12_btn.color
        self.options["color13"] = self.color13_btn.color
        self.options["color14"] = self.color14_btn.color

        self.options["TranslateSnap"] = float(self.t_snap_line.text())
        self.options["RotateSnap"] = float(self.r_snap_line.text())
        self.options["ScaleSnap"] = float(self.s_snap_line.text())
        if self.world_radio.isChecked(): self.options["Space"] = "world"
        elif self.object_radio.isChecked(): self.options["Space"] = "object"
        option_path = os.path.join(os.path.dirname(__file__), "json", "options.json")
        with open(option_path, "w") as f:
            json.dump(self.options, f, indent=4)

    def options_window(self):
        self.options_dialog.exec_()

    def set_custom_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            print("red: {0}, green: {1}, blue: {2}".format(*color.getRgb()))
            self.custom_color_btn.setStyleSheet("background-color:rgb({0},{1},{2})".format(*color.getRgb()))
            self.custom_color_btn.color = color
            shapes = [ y for x in pm.selected(type="transform") for y in x.getShapes() ]
            for shape in shapes:
                shape.overrideEnabled.set(True)
                shape.overrideRGBColors.set(True)
                shape.overrideColorRGB.set((color.getRgb()[0]/255.0, color.getRgb()[1]/255.0, color.getRgb()[2]/255.0))
        else:
            self.custom_color_btn.setStyleSheet("")
            self.custom_color_btn.color = None

    def controller_controller(self, attrs):
        with UndoInfo():
            lock, unlock, hide, unhide, nonkey, key, plus, minus = range(8)
            if self.lock_radio.isChecked(): mode = lock
            elif self.unlock_radio.isChecked(): mode = unlock
            elif self.hide_radio.isChecked(): mode = hide
            elif self.unhide_radio.isChecked(): mode = unhide
            elif self.nonkey_radio.isChecked(): mode = nonkey
            elif self.key_radio.isChecked(): mode = key
            elif self.plus_radio.isChecked(): mode = plus
            elif self.minus_radio.isChecked(): mode = minus
            transform_node = pm.ls(selection=True, type="transform")
            
            reg = "".join(attrs)
            if "t" in reg:
                if "x" in reg: x = float(self.t_snap_line.text())
                else: x = 0
                if "y" in reg: y = float(self.t_snap_line.text())
                else: y = 0
                if "z" in reg: z = float(self.t_snap_line.text())
                else: z = 0
            if "r" in reg:
                if "x" in reg: x = float(self.r_snap_line.text())
                else: x = 0
                if "y" in reg: y = float(self.r_snap_line.text())
                else: y = 0
                if "z" in reg: z = float(self.r_snap_line.text())
                else: z = 0
            if "s" in reg:
                if "x" in reg: x = float(self.s_snap_line.text())
                else: x = 0
                if "y" in reg: y = float(self.s_snap_line.text())
                else: y = 0
                if "z" in reg: z = float(self.s_snap_line.text())
                else: z = 0

            if mode == minus:
                x = -1 * x
                y = -1 * y
                z = -1 * z
                
            if (mode == minus) or (mode == plus):
                if "v" in attrs:
                    return
                cvs = list()
                for node in transform_node:
                    for shape in node.getShapes():
                        cvs.append(shape.cv)
                pm.select(cvs)

                if self.object_radio.isChecked():
                    if "t" in reg:
                        pm.move((x, y, z), relative=True, objectSpace=True, worldSpaceDistance=True)
                    if "r" in reg:
                        pm.rotate((x, y, z), relative=True, objectSpace=True, objectCenterPivot=True, forceOrderXYZ=True)   
                    if "s" in reg:
                        pm.scale((1+x, 1+y, 1+z), relative=True, objectSpace=True, objectCenterPivot=True)
                elif self.world_radio.isChecked():
                    if "t" in reg:
                        pm.move((x, y, z), relative=True)
                    if "r" in reg:
                        pm.rotate((x, y, z), relative=True, worldSpace=True, objectCenterPivot=True, forceOrderXYZ=True)
                    if "s" in reg:
                        pm.scale((1+x, 1+y, 1+z), relative=True, worldSpace=True, objectCenterPivot=True)
                pm.select(transform_node)
                return

            for node in transform_node:
                for attr in attrs:
                    if mode == lock:
                        node.attr(attr).lock()
                    elif mode == unlock:
                        node.attr(attr).unlock()
                    elif mode == hide:
                        node.attr(attr).setKeyable(False)
                    elif mode == unhide:
                        node.attr(attr).setKeyable(True)
                    elif mode == nonkey:
                        node.attr(attr).set(channelBox=True)
                    elif mode == key:
                        node.attr(attr).setKeyable(True)
    
    def get_shapes(self, name):
        selected_nodes = pm.ls(selection=True)
        combine_curve = self.combine_shapes(selected_nodes)
        pm.delete(combine_curve, constructionHistory=True)
        shapes = combine_curve.getShapes()

        create_curve_string = "#-*- coding:utf-8 -*-\n\n"
        create_curve_string += "import pymel.core as pm\n\n\n"
        create_curve_string += "def create_controller():\n"
        create_curve_string += "\tcurves = list()\n"

        curve_argument = str()
        for shape in shapes:
            degree = shape.degree()
            period = shape.f.get()
            knots = shape.getKnots()
            points = [ x.totuple() for x in shape.getCVs() ]
            curve_argument += "\tcurves.append(pm.curve(p={0}, d={1}, per={2}, k={3}))\n".format(
                points, degree, period, knots)

        create_curve_string += curve_argument
        create_curve_string += "\tpm.makeIdentity(curves, a=1, t=1, r=1, s=1, n=0, pn=1)\n"
        create_curve_string += "\tempty_grp = pm.group(name='{0}', empty=True)\n".format(name)
        create_curve_string += "\tshapes = [ y for x in curves for y in x.getShapes() ]\n"
        create_curve_string += "\tpm.parent(shapes, empty_grp, relative=True, shape=True)\n"
        create_curve_string += "\tpm.delete(curves)\n"
        create_curve_string += "\tshapes = empty_grp.getShapes()\n"
        create_curve_string += "\tfor index, shape in enumerate(shapes):\n"
        create_curve_string += "\t\tif index == 0: index = str()\n"
        create_curve_string += "\t\tshape.rename('{0}Shape{1}'.format(empty_grp.name(), index))\n"
        create_curve_string += "\treturn empty_grp"
        return create_curve_string

    def combine_shapes(self, controllers):
        pm.makeIdentity(controllers, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
        empty_grp = pm.group(empty=True)
        shapes = [ y for x in controllers for y in x.getShapes() if "Orig" not in y.name()]
        pm.parent(shapes, empty_grp, relative=True, shape=True)
        pm.delete(controllers)
        pm.select(empty_grp)
        return empty_grp

    def get_curve_color(self, controllers):
        if not controllers:
            return
        shapes = [ x.getShape() for x in controllers]
        colors = list()
        for shape in shapes:
            if shape.overrideEnabled.get():
                if shape.overrideRGBColors.get():
                    colors.append(shape.overrideColorRGB.get())
                else:
                    colors.append(shape.overrideColor.get())
            else:
                colors.append(list())
        return colors

    def set_curve_color(self, controllers, colors):
        shapes_list = [ x.getShapes() for x in controllers ]

        for index, shapes in enumerate(shapes_list):
            for shape in shapes:
                if issubclass(type(colors[index]), int):
                    shape.overrideEnabled.set(True)
                    shape.overrideRGBColors.set(False)
                    shape.overrideColor.set(colors[index])
                elif issubclass(type(colors[index]), tuple):
                    shape.overrideEnabled.set(True)
                    shape.overrideRGBColors.set(True)
                    shape.overrideColorRGB.set(colors[index])

    def reload(self):
        collection_path = os.path.join(os.path.dirname(__file__), "collection")
        if collection_path not in sys.path:
            sys.path.append(collection_path)
        list_dir = os.listdir(collection_path)

        info = dict()
        for f in list_dir:
            if os.path.splitext(f)[-1] == ".py":
                info[os.path.splitext(f)[0]] = {
                    "py" : os.path.join(collection_path, f),
                    "jpg" : os.path.join(collection_path, f.replace(".py", ".0001.jpg"))
                }
        
        self.listWidget.clear()
        for key, value in info.items():
            item = QtWidgets.QListWidgetItem(key)
            icon = QtGui.QIcon(value["jpg"])
            item.setIcon(icon)
            self.listWidget.addItem(item)

    def save_controller(self):
        with UndoInfo():
            name = self.name_line.text()
            if not name:
                return
            if not pm.ls(selection=True):
                return

            py_path = os.path.join(os.path.dirname(__file__), "collection", "{0}.py".format(name))
            ss_path = os.path.join(os.path.dirname(__file__), "collection", "{0}".format(name))

            if os.path.isfile(py_path):
                messagebox = QtWidgets.QMessageBox()
                messagebox.setText("정말로 {0}을/를 교체하시겠습니까?".format(name))
                messagebox.setInformativeText("Do you want to change {0}?".format(name))
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel)
                messagebox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                result = messagebox.exec_()
                if result == QtWidgets.QMessageBox.Save:
                    pass
                elif result ==  QtWidgets.QMessageBox.Cancel:
                    return


            txt = self.get_shapes(name=name)
            with open(py_path, "w") as f:
                f.write(txt)

            selected_nodes = pm.ls(selection=True)
            shapes = selected_nodes[0].getShapes()
            for shape in shapes:
                shape.lineWidth.set(10)
                shape.overrideEnabled.set(True)
                shape.overrideColor.set(16)

            current_time = pm.currentTime()
            pm.select(clear=True)
            pm.playblast(
                startTime=current_time, 
                endTime=current_time, 
                format="image", 
                filename=ss_path,
                sequenceTime=0,
                clearCache=0,
                viewer=0,
                showOrnaments=0,
                framePadding=4,
                percent=100,
                compression="jpg",
                quality=100,
                widthHeight=(1024, 1024)
                )   
            pm.select(selected_nodes)

            for shape in shapes:
                shape.lineWidth.set(-1)
                shape.overrideEnabled.set(False)
            
            self.reload()

    def load_controller(self):
        with UndoInfo():
            selected_item = self.listWidget.selectedItems()
            if not selected_item:
                return
            name = selected_item[0].text()

            fileName = importlib.import_module(name)
            reload(fileName)
            selected = pm.selected(type="transform")
            if not selected:
                return fileName.create_controller()
            controllers = list()
            for index, sel in enumerate(selected):
                controllers.append(fileName.create_controller())
                pm.matchTransform(controllers[index], sel)
            return controllers

    def delete_controller(self):
        selected_item = self.listWidget.selectedItems()
        if not selected_item:
            return
        name = selected_item[0].text()

        collection_path = os.path.join(os.path.dirname(__file__), "collection")
        py = os.path.join(collection_path, "{0}.py".format(name))
        pyc = os.path.join(collection_path, "{0}.pyc".format(name))
        jpg = os.path.join(collection_path, "{0}.0001.jpg".format(name))

        messagebox = QtWidgets.QMessageBox()
        messagebox.setText("정말로 {0}을/를 삭제하시겠습니까?".format(name))
        messagebox.setInformativeText("Do you want to delete {0}?".format(name))
        messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        messagebox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        result = messagebox.exec_()
        if result == QtWidgets.QMessageBox.Ok: 
            if os.path.isfile(py):
                os.remove(py)
            if os.path.isfile(jpg):
                os.remove(jpg)
            if os.path.isfile(pyc):
                os.remove(pyc)
            self.reload()
        elif result ==  QtWidgets.QMessageBox.Cancel:
            return

    def replace_shape(self):
        with UndoInfo():
            selected_nodes = pm.ls(selection=True)
            selected_nodes_shapes = [ shape.getShapes() for shape in selected_nodes ]
            controllers_norm = list()
            for shapes in selected_nodes_shapes:
                if shapes:
                    cvs = list()
                    for shape in shapes:
                        cvs.extend(shape.getCVs(space="world"))
                    bbmin = np.amin(cvs, axis=0)
                    bbmax = np.amax(cvs, axis=0)
                    controllers_norm.append(np.linalg.norm(bbmax - bbmin))
                else:
                    controllers_norm.append(None)
            
            controllers_colors = self.get_curve_color(selected_nodes)
                
            new_controllers = list()
            pm.select(clear=True)
            for i in selected_nodes:
                new_controllers.append(self.load_controller())
            boundingbox = [
                new_controllers[0].getBoundingBox().width(),
                new_controllers[0].getBoundingBox().height(),
                new_controllers[0].getBoundingBox().depth(),
                ]
            new_controller_norm = np.linalg.norm(boundingbox)
            for index, new_controller in enumerate(new_controllers):
                scale = controllers_norm[index] / new_controller_norm
                new_controller.s.set(scale, scale, scale)
            pm.makeIdentity(new_controllers, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
            pm.delete([ y for x in selected_nodes_shapes for y in x ])

            for index, new in enumerate(new_controllers):
                shapes = new.getShapes()
                pm.parent(shapes, selected_nodes[index], relative=True, shape=True)
                for number, shape in enumerate(shapes):
                    if number == 0: number = str()
                    shape.rename("{0}Shape{1}".format(selected_nodes[index].name(), number))

            self.set_curve_color(selected_nodes, controllers_colors)
            pm.delete(new_controllers)
            pm.select(selected_nodes)

    def mirror_shape(self):
        with UndoInfo():
            selected_nodes = pm.ls(selection=True, type="transform")

            controllers = list()
            rev_controllers = list()
            for index, node in enumerate(selected_nodes):
                for key, value in self.options["MirrorFilter"].items():
                    if len(controllers) > index:
                        continue
                    left_reg = re.compile(r"^{string}\d+_\w+|\w+_{string}\d+_\w+|^{string}_\w+|\w+_{string}_\w+|\w+_{string}\d+|\w+_{string}".format(string=key))
                    right_reg = re.compile(r"^{string}\d+_\w+|\w+_{string}\d+_\w+|^{string}_\w+|\w+_{string}_\w+|\w+_{string}\d+|\w+_{string}".format(string=value))

                    if left_reg.search(node.name()):
                        split_name = node.name().split()
                        name = None
                        for i in range(len(split_name)):
                            temp = node.name().split()
                            temp[i] = temp[i].replace(key, value)
                            name = "_".join(temp)
                            if pm.objExists(name):
                                controllers.append(node)
                                rev_controllers.append(pm.PyNode(name))
                                break
                    elif right_reg.search(node.name()):
                        split_name = node.name().split()
                        name = None
                        for i in range(len(split_name)):
                            temp = node.name().split()
                            temp[i] = temp[i].replace(value, key)
                            name = "_".join(temp)
                            if pm.objExists(name):
                                controllers.append(node)
                                rev_controllers.append(pm.PyNode(name))
                                break
                if len(controllers) == index:
                    controllers.append(None)
                    rev_controllers.append(None)
                        
            for index, con in enumerate(controllers):
                if con in rev_controllers:
                    controllers.remove(con)
                    rev_controllers.remove(rev_controllers[index])

            controllers = filter(None, controllers)
            rev_controllers = filter(None, rev_controllers)

            colors_rev_controllers = self.get_curve_color(rev_controllers)

            rev_controllers_shapes = [ shape.getShapes() for shape in rev_controllers ]

            pm.delete([ y for x in rev_controllers_shapes for y in x ])

            for index, con in enumerate(controllers):
                dup_shapes = [ pm.PyNode(pm.duplicateCurve(x, constructionHistory=False)[0]) for x in con.getShapes() ]
                pm.matchTransform(dup_shapes, con, rot=True)
                pm.matchTransform(dup_shapes, rev_controllers[index], pos=True)
                pm.parent(dup_shapes, rev_controllers[index])

                select_cv = [ x.cv[:] for x in dup_shapes ]
                pm.select(select_cv)

                pm.scale((-1, 1, 1), worldSpace=True)
                pm.makeIdentity(dup_shapes, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)

                pm.parent([ x.getShape() for x in dup_shapes ], rev_controllers[index], relative=True, shape=True)
                pm.delete(dup_shapes)
                for number, shape in enumerate(rev_controllers[index].getShapes()):
                    if number == 0: number = str()
                    shape.rename("{0}Shape{1}".format(rev_controllers[index].name(), number))
            
            self.set_curve_color(rev_controllers, colors_rev_controllers)
            pm.select(selected_nodes)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseMove and obj is self.custom_color_btn:
            if obj.color:
                mimedata = QtCore.QMimeData()
                mimedata.setColorData(obj.color)
                
                pixmap = QtGui.QPixmap(20, 20)
                pixmap.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(pixmap)
                painter.setRenderHint(QtGui.QPainter.Antialiasing)
                painter.setBrush(obj.color)
                painter.setPen(QtGui.QPen(obj.color.darker(150), 2))
                painter.drawEllipse(pixmap.rect().center(), 8, 8)
                painter.end()
                
                drag = QtGui.QDrag(obj)
                drag.setMimeData(mimedata)
                drag.setPixmap(pixmap)
                drag.setHotSpot(pixmap.rect().center())
                drag.exec_(QtCore.Qt.CopyAction)
                self.custom_color_btn.setDown(False)
                return True
            
        elif event.type() == QtCore.QEvent.DragEnter:
            event.accept() if event.mimeData().hasColor() else event.ignore()

        elif event.type() == QtCore.QEvent.Drop:
            if not (obj is self.custom_color_btn):
                obj.color = event.mimeData().colorData().getRgb()[:3]
                obj.setStyleSheet("background-color:rgb({0},{1},{2})".format(*obj.color))
                self.save_options()
                event.accept()

        return super(Moyang, self).eventFilter(obj, event)