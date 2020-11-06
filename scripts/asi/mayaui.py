# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from coreui import AsiListView, AsiTableView, AsiTableModel, AsiTableDelegate
from mworkspacecontrol import MWorkspaceControl
from functools import partial

import pymel.core as pm
import json
import os
import pprint


class AsiMayaTableView(AsiTableView):

    asi_clicked = QtCore.Signal(QtCore.QModelIndex)
    asi_double_clicked = QtCore.Signal(QtCore.QModelIndex)
    asi_shelf_clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(AsiMayaTableView, self).__init__(parent=parent)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_number = 0
        self.index = None

    def mousePressEvent(self, event):
        super(AsiMayaTableView, self).mousePressEvent(event)
        self.index1 = self.indexAt(event.pos())
        if self.index1.isValid():
            if event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                self.asi_shelf_clicked.emit(self.index1)
                return
        self.click_number += 1
        if not self.timer.isActive():
            self.timer.start()

    def mouseDoubleClickEvent(self, event):
        super(AsiMayaTableView, self).mouseDoubleClickEvent(event)
        if self.timer.isActive():
            self.click_number += 1
            self.index2 = self.indexAt(event.pos())
        
    def timeout(self):
        if self.click_number == 1:
            self.asi_clicked.emit(self.index1)
        elif (self.click_number == 2) & (self.index1 == self.index2):
            self.asi_double_clicked.emit(self.index1)
        self.click_number = 0


class AsiMayaListView(AsiListView):
    
    def __init__(self, parent=None):
        super(AsiMayaListView, self).__init__(parent=parent)
    
    def mousePressEvent(self, event):
        super(AsiMayaListView, self).mousePressEvent(event)


class AsiMaya(QtWidgets.QMainWindow):
    
    __permission = None
    ui_admin_instance = None
    ui_guest_instance = None

    python_icon = "pythonFamily.png"
    mel_icon = "commandButton.png"

    @classmethod
    def display(cls, permission):
        if permission == "admin":
            if cls.ui_admin_instance:
                cls.ui_admin_instance.show_workspace_control()
            else:
                cls.ui_admin_instance = cls(permission=permission)
        elif permission == "guest":
            if cls.ui_guest_instance:
                cls.ui_guest_instance.show_workspace_control()
            else:
                cls.ui_guest_instance = cls(permission=permission)

    @classmethod
    def get_workspace_control_name(cls, permission):
        return '{0}{1}WorkspaceControl'.format(cls.__name__, permission)

    @classmethod
    def get_ui_script(cls, permission):
        ui_script = "from {0} import {1}\n{1}.display('{2}')".format(cls.__module__, cls.__name__, permission)
        return ui_script
    
    def create_workspace_control(self, permission):
        self.workspace_control_instance = MWorkspaceControl(self.get_workspace_control_name(permission))
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.__class__.__name__, self, ui_script=self.get_ui_script(permission=permission))

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)

    @property
    def permission(self):
        return self.__permission
    
    @permission.setter
    def permission(self, p):
        self.__permission = p

    def __init__(self, permission="guest", parent=None):
        super(AsiMaya, self).__init__(parent=parent)
        self.permission = permission

        self.setObjectName("{0}{1}".format(self.__class__.__name__, self.permission))
        self.create_widgets()
        self.create_connections()
        self.load_json()
        self.create_workspace_control(permission=self.permission)

    def create_widgets(self):
        self.ad = QtWidgets.QDialog()
        self.ed = QtWidgets.QDialog()
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "main.ui"), self)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "maya_item.ui"), self.ad)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "maya_item.ui"), self.ed)

        self.table_view = AsiMayaTableView()
        self.list_view = AsiMayaListView()
        self.view_layout.addWidget(self.table_view)
        self.view_layout.addWidget(self.list_view)
        self.table_view.setItemDelegate(AsiTableDelegate())
        self.table_view.setModel(AsiTableModel())
        self.table_view.horizontalHeader().hideSection(4)
        
        self.view_mode_action_group = QtWidgets.QActionGroup(self)
        self.view_mode_action_group.addAction(self.action_table)
        self.view_mode_action_group.addAction(self.action_list)
        self.action_table.setChecked(True)
        self.list_view.hide()
        
        if self.permission == "guest":  
            self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            return
        self.add_item_action = QtWidgets.QAction("add item" , self)
        self.edit_item_action = QtWidgets.QAction("edit item", self)
        self.delete_item_action = QtWidgets.QAction("delete item", self)

    def create_connections(self):
        self.view_mode_action_group.triggered.connect(self.view_mode)
        self.ad.accepted.connect(self.add_item)
        self.ed.accepted.connect(self.edit_item)
        self.load_action_btn.triggered.connect(self.load_json)
        self.save_action_btn.triggered.connect(self.save_json)

        if self.permission == "guest":
            self.table_view.asi_clicked[QtCore.QModelIndex].connect(self.run_click_command)
            self.table_view.asi_double_clicked[QtCore.QModelIndex].connect(self.run_double_click_command)
            self.table_view.asi_shelf_clicked[QtCore.QModelIndex].connect(self.add_shelf_button)
            return
        self.table_view.customContextMenuRequested[QtCore.QPoint].connect(self.table_view_menu)
        self.add_item_action.triggered.connect(self.add_item_window)
        self.edit_item_action.triggered.connect(self.edit_item_window)
        self.delete_item_action.triggered.connect(self.delete_item)

    def view_mode(self):
        if self.action_table.isChecked(): 
            self.table_view.show()
            self.list_view.hide()
        elif self.action_list.isChecked(): 
            self.table_view.hide()
            self.list_view.show()

    def table_view_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addActions([self.add_item_action, self.edit_item_action, self.delete_item_action])
        context_menu.exec_(self.table_view.mapToGlobal(point))

    def add_item_window(self):
        self.ad.author_line.clear()
        self.ad.label_line.clear()
        self.ad.overlay_label_line.clear()
        self.ad.image_line.clear()
        self.ad.python_radio_btn.setChecked(True)
        self.ad.command_text.clear()
        self.ad.double_click_command_text.clear()
        self.ad.annotation_text.setText("Requested\t: \nPurpose \t: ")

        self.ad.exec_()
    
    def edit_item_window(self):
        current_item = self.table_view.currentIndex()
        
        if not current_item.isValid():
            return

        label = current_item.data(self.label_role)
        imageOverlayLabel = current_item.data(self.image_label_role)
        image = current_item.data(self.image_role)
        sourceType = current_item.data(self.source_type_role)
        command = current_item.data(self.command_role)
        doubleClickCommand = current_item.data(self.double_command_role)
        annotation = current_item.data(self.annotation_role)

        self.ad.label_line.setText(label)
        if sourceType == "python":
            self.ad.python_radio_btn.setChecked(True)
        else:
            self.ad.mel_radio_btn.setChecked(True)
        self.ad.overlay_label_line.setText(imageOverlayLabel)
        self.ad.image_line.setText(image)
        self.ad.command_text.setPlainText(command)
        self.ad.double_click_command_text.setPlainText(doubleClickCommand)
        self.ad.annotation_text.setPlainText(annotation)

        self.ad.exec_()
    
    def add_item(self):
        author = self.ad.author_line.text()
        label = self.ad.label_line.text()
        if self.ad.python_radio_btn.isChecked():
            source_type = "python"
        if self.ad.mel_radio_btn.isChecked():
            source_type = "mel"
        overlay_label = self.ad.overlay_label_line.text()
        if self.ad.image_line.text():
            image = self.ad.image_line.text()
        else:
            if source_type == "python":
                image = self.python_icon
            else:
                image = self.mel_icon
        command = self.ad.command_text.toPlainText()
        double_click_command = self.ad.double_click_command_text.toPlainText()
        annotation = self.ad.annotation_text.toPlainText()
        
        data = list()
        data.append(":{0}".format(image))
        data.append(label)
        data.append(author)
        data.append(list())
        meta = {"sourceType" : source_type,
                "command" : command,
                "doubleCommand" : double_click_command,
                "annotation" : annotation,
                "overlayLabel" : overlay_label}
        data.append(meta)
        model = self.table_view.model()
        model.insertRows(position=model.rowCount(), data=data)

    def edit_item(self):
        print "TODO"

    def delete_item(self):
        model = self.table_view.model()
        current_index = self.table_view.currentIndex()
        pos = current_index.row()
        model.removeRows(pos)
        tags_set = set()
        for row in range(model.rowCount()):
            tags = model.data(index=model.index(row, 3), role=QtCore.Qt.DisplayRole)
            for tag in tags:
                tags_set.add(tag)
        colors = model.colors
        tags_color = colors.keys()
        for tag in tags_color:
            if tag not in tags_set:
                del colors[tag]
        model.setData(QtCore.QModelIndex(), colors, QtCore.Qt.UserRole)

    def save_json(self):
        model = self.table_view.model()
        with open(os.path.join(os.path.dirname(__file__), "json", "colors.json"), "w") as f: 
            json.dump(model.colors, f)
        
        data = dict()
        temp = model.scripts
        for index in range(len(temp)):
            data[unicode(index)] = {"Icon":temp[index][0], 
                                "Label":temp[index][1], 
                                "Author":temp[index][2], 
                                "Tags":temp[index][3], 
                                "Meta":temp[index][4]}
        with open(os.path.join(os.path.dirname(__file__), "json", "maya.json"), "w") as f: 
            json.dump(data, f)
        pprint.pprint(data)
        pprint.pprint(model.colors)

    def load_json(self):
        with open(os.path.join(os.path.dirname(__file__), "json", "colors.json")) as f: 
            colors = json.load(f)
        
        with open(os.path.join(os.path.dirname(__file__), "json", "maya.json")) as f: 
            scripts = json.load(f)
        model = self.table_view.model()
        model.reset()
        model.colors = colors

        for index in sorted([x for x in scripts]):
            data = list()
            data.append(scripts[index]["Icon"])
            data.append(scripts[index]["Label"])
            data.append(scripts[index]["Author"])
            data.append(scripts[index]["Tags"])
            data.append(scripts[index]["Meta"])
            model.insertRows(position=int(index), data=data)
        pprint.pprint(scripts)
        pprint.pprint(colors)

    def run_click_command(self, index):
        if not index.isValid():
            return
        model = self.table_view.model()
        meta_data = model.data(index=model.index(index.row(), 4), role=QtCore.Qt.DisplayRole)
        
        source_type = meta_data["sourceType"]
        command = meta_data["command"]
        if source_type == "python":
            pm.undoInfo(openChunk=True)
            exec(command)
            pm.undoInfo(closeChunk=True)
        else:
            pm.undoInfo(openChunk=True)
            pm.mel.eval(command)
            pm.undoInfo(closeChunk=True)
        
    def run_double_click_command(self, index):
        if not index.isValid():
            return
        model = self.table_view.model()
        meta_data = model.data(index=model.index(index.row(), 4), role=QtCore.Qt.DisplayRole)
        
        source_type = meta_data["sourceType"]
        command = meta_data["doubleCommand"]
        if source_type == "python":
            pm.undoInfo(openChunk=True)
            exec(command)
            pm.undoInfo(closeChunk=True)
        else:
            pm.undoInfo(openChunk=True)
            pm.mel.eval(command)
            pm.undoInfo(closeChunk=True)

    def add_shelf_button(self, index):
        if not index.isValid():
            return
        model = self.table_view.model()

        icon = model.data(index=model.index(index.row(), 0), role=QtCore.Qt.DisplayRole)
        label = model.data(index=model.index(index.row(), 1), role=QtCore.Qt.DisplayRole)
        meta = model.data(index=model.index(index.row(), 4), role=QtCore.Qt.DisplayRole)
        imageoverlay_label = meta["overlayLabel"]
        source_type = meta["sourceType"]
        command = meta["command"]
        double_command = meta["doubleCommand"]
        annotation = meta["annotation"]

        current_tab = pm.tabLayout("ShelfLayout", query=True, selectTab=True)

        if icon == ":{0}".format(self.python_icon):
            icon = self.python_icon
        elif icon == ":{0}".format(self.mel_icon):
            icon = self.mel_icon

        pm.shelfButton(parent=current_tab,
                        image=icon,
                        command=command, 
                        doubleClickCommand=double_command,
                        label=label,
                        imageOverlayLabel=imageoverlay_label,
                        sourceType=source_type,
                        annotation=annotation)
                
