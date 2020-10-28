# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from functools import partial
# from .TagLines import TagLine

import random
import json
import os

tag_role = QtCore.Qt.UserRole + 1
color_role = QtCore.Qt.UserRole + 2


class AsiCoreUI(QtWidgets.QMainWindow):
    
    __table_view_delegate = None
    __table_view_model = None

    @property
    def table_view_delegate(self):
        return self.__table_view_delegate
    
    @table_view_delegate.setter
    def table_view_delegate(self, t):
        self.__table_view_delegate = t

    @property
    def table_view_model(self):
        return self.__table_view_model
    
    @table_view_model.setter
    def table_view_model(self, m):
        self.__table_view_model = m

    def __init__(self, parent=None):
        super(AsiCoreUI, self).__init__(parent=parent)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "main.ui"), self)

        self.table_view_delegate = AsiTableDelegate(self.table_view)
        self.table_view_model = AsiTableModel()
        self.table_view.setItemDelegate(self.table_view_delegate)
        self.table_view.setModel(self.table_view_model)
        self.table_view.setColumnWidth(1, 70)
        self.table_view.setColumnWidth(2, 100)
        
        self.view_mode_action_group = QtWidgets.QActionGroup(self)
        self.view_mode_action_group.addAction(self.action_table)
        self.view_mode_action_group.addAction(self.action_list)
        self.action_table.setChecked(True)
        self.list_view.hide()

        self.view_mode_action_group.triggered.connect(self.view_mode)

    def view_mode(self):
        if self.action_table.isChecked(): self.table_view.show(); self.list_view.hide()
        elif self.action_list.isChecked(): self.table_view.hide(); self.list_view.show()

    def save_json(self, data, path):
        with open(path, "w") as f: json.dump(data, f)
        
    def load_json(self, path):
        with open(path) as f: data = json.load(f)
        return data
    
    def refresh(self, colors, scripts):
        self.table_view_model.reset()
        self.table_view_delegate.colors = colors

        for row, label in enumerate(scripts):
            item = list()
            item.append(scripts[label]["Icon"])
            item.append(label)
            item.append(scripts[label]["Author"])
            item.append(scripts[label]["Tags"])
            # item.append(scripts[label]["Meta"])
            self.table_view_model.insertRows(row, data=item)
            # self.table_view.insertRow(row)
            # icon_item = QtWidgets.QTableWidgetItem()
            # icon_item.setIcon(QtGui.QIcon(scripts[item]["Icon"]))
            # self.table_view.setItem(row, 0, icon_item)
            # self.table_view.setItem(row, 1, QtWidgets.QTableWidgetItem(item))
            # self.table_view.setItem(row, 2, QtWidgets.QTableWidgetItem(scripts[item]["Author"]))
            # TagLine_item = QtWidgets.QTableWidgetItem()
            # TagLine_item.setData(tag_role, scripts[item]["Tags"])
            # self.table_view.setItem(row, 3, TagLine_item)

    def load_item_data(self):
        data = dict()
        return data


class AsiTableDelegate(QtWidgets.QStyledItemDelegate):
    
    __colors = None

    @property
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c

    def __init__(self, parent=None):
        super(AsiTableDelegate, self).__init__(parent)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        if index.column() == 0:
            icon = QtGui.QIcon(index.data())
            icon.paint(painter, option.rect, QtCore.Qt.AlignCenter)
            # QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        elif index.column() == 3: 
            editor = TagsEditor()

            if option.state & QtWidgets.QStyle.State_Selected:
                painter.fillRect(option.rect, painter.brush())
            
            painter.save()
            editor.colors = self.colors
            editor.setup_ui(index.data())
            editor.vis_button(switch=False)
            
            painter.translate(option.rect.topLeft())
            editor.resize(option.rect.size())
            editor.render(painter, QtCore.QPoint(0, 0))
            painter.restore()
            # QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        if index.column() == 1:
            return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        elif index.column() == 3:
            editor = TagsEditor()
            editor.colors = self.colors
            editor.setup_ui(index.data())
            return editor.sizeHint()
        else:
            return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)

    def createEditor(self, parent, option, index):
        """ Creates and returns the custom StarEditor object we'll use to edit 
            the StarRating.
        """
        if index.column() == 3:
            editor = TagsEditor(parent=parent)
            editor.colors = self.colors
            editor.setup_ui(index.data())
            editor.vis_button(switch=True)
            return editor
        else:
            return QtWidgets.QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """ Sets the data to be displayed and edited by our custom editor. """
        if index.column() == 3:
            pass
            # editor.colors = self.colors
            # editor.setup_ui(index.data()[3])
            # editor.vis_button(switch=True)
        else:
            QtWidgets.QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """ Get the data from our custom editor and stuffs it into the model.
        """
        if index.column() == 3:
            model.setData(index, editor.tags, QtCore.Qt.EditRole)
            self.colors = editor.colors
        else:
            QtWidgets.QStyledItemDelegate.setModelData(self, editor, model, index)


class AsiTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, asi_data=None, parent=None):
        super(AsiTableModel, self).__init__(parent)
        if asi_data is None: self.asi_data = list()
        else: self.asi_data = asi_data # [icon, label, author, tags, meta]

    def reset(self):
        self.beginResetModel()
        self.asi_data = list() 
        self.endResetModel()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.asi_data)
    
    def columnCount(self, index=QtCore.QModelIndex()):
        return 4
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.asi_data[index.row()][index.column()]
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        return None

    def setData(self, index, value, role=None):
        if role != QtCore.Qt.EditRole:
            return False
        
        if index.isValid() and 0 <= index.row() < len(self.asi_data):
            # for i in range(index.column()-1):
                # print self.asi_data[index.column()]
            self.asi_data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True

        return False
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Icon"
            elif section == 1:
                return "Label"
            elif section == 2:
                return "Author"
            elif section == 3:
                return "Tags"
        return None

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex(), data=None):
        self.beginInsertRows(QtCore.QModelIndex(), position, position+rows-1)

        for row in range(rows):
            self.asi_data.insert(position+row, data)

        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)

        del self.asi_data[position:position+rows]

        self.endRemoveRows()
        return True

class TagsEditor(QtWidgets.QWidget):

    __colors = None

    @property
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c

    def __init__(self, parent=None):
        super(TagsEditor, self).__init__(parent)
        
        self.tags = list()
        self.x_buttons = list()
        self.create_ui()

    def create_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self) # TODO : custom layout
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.tag_layout = QtWidgets.QHBoxLayout()
        self.tag_layout.setContentsMargins(4, 4, 4, 4)
        self.tag_layout.setSpacing(6)

        self.line_layout = QtWidgets.QHBoxLayout()
        self.line_layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addLayout(self.tag_layout)
        self.layout.addLayout(self.line_layout)
        self.layout.addStretch(True)

        self.line = QtWidgets.QLineEdit()
        self.line.returnPressed.connect(self.entered_line)
        self.line_layout.addWidget(self.line)
        self.line.hide()

        self.spacer = QtWidgets.QSpacerItem(4, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Base)

    def create_tag(self, name, color):
        count = self.tag_layout.count()
        if count > 0:
            spacer = self.tag_layout.takeAt(count-1)
            del spacer
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("QFrame {{\nbackground-color: hsva({0}, 100, 222, 255);\nborder-radius: 4px;\n}}".format(color))
        frame.setFixedHeight(24)
        label = QtWidgets.QLabel(name)
        label.setStyleSheet("QLabel {\ncolor: #000000;}")
        label.setAlignment(QtCore.Qt.AlignCenter)
        button = QtWidgets.QPushButton("X")
        button.setFixedSize(16, 16)
        
        frame_layout = QtWidgets.QHBoxLayout(frame)
        frame_layout.addWidget(label)
        frame_layout.addWidget(button)
        frame_layout.setContentsMargins(4, 4, 4, 4)
        frame_layout.setSpacing(4)

        self.tag_layout.addWidget(frame)
        self.tag_layout.insertSpacerItem(-1, self.spacer)
        button.clicked.connect(partial(self.delete_tag, tag=frame, name=name))
        self.x_buttons.append(button)
        self.tags.append(name)

    def vis_button(self, switch):
        if switch is True: 
            self.line.show()
            for button in self.x_buttons: button.show()
        elif switch is False: 
            self.line.hide()
            for button in self.x_buttons: button.hide()
        self.setMinimumSize(self.layout.sizeHint())

    def delete_tag(self, tag, name):
        tag.hide()
        self.tags.remove(name)
    
    def setup_ui(self, data):
        for tag in data: self.create_tag(name=tag, color=self.colors[tag])
    
    def entered_line(self):
        txt = self.line.text()
        if not txt:
            return
        check_list = set()
        for s in txt:
            if " " == s:
                check_list.add(True)
            else:
                check_list.add(False)
        if len(check_list) > 1:
            return
        if txt in self.tags:
            return

        if self.colors.has_key(txt):
            color = self.colors[txt]
        else:
            color = random.randint(0, 360)
            self.colors[txt] = color
        self.create_tag(name=txt, color=color)
        self.line.clear()


            

        




























from mworkspacecontrol import MWorkspaceControl
import pymel.core as pm

class AsiMayaUI(AsiCoreUI):
    
    __colors = None
    __scripts = None
    __permission = None
    python_icon = "pythonFamily.png"
    mel_icon = "commandButton.png"
    ui_admin_instance = None
    ui_guest_instance = None

    @property
    def permission(self):
        return self.__permission
    
    @permission.setter
    def permission(self, p):
        self.__permission = p

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
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c
    
    @property
    def scripts(self):
        return self.__scripts
    
    @scripts.setter
    def scripts(self, s):
        self.__scripts = s

    def __init__(self, permission="guest", parent=None):
        super(AsiMayaUI, self).__init__(parent=parent)
        self.permission = permission

        self.colors = self.load_json(path=os.path.join(os.path.dirname(__file__), "json", "colors.json"))
        self.scripts = self.load_json(path=os.path.join(os.path.dirname(__file__), "json", "maya.json"))
        self.refresh(colors=self.colors, scripts=self.scripts)

        self.setObjectName("{0}{1}".format(self.__class__.__name__, self.permission))
        self.create_workspace_control(permission=permission)
        self.ad = QtWidgets.QDialog()
        self.add_item_action = QtWidgets.QAction("add item" , self)
        self.edit_item_action = QtWidgets.QAction("edit item", self)
        self.delete_item_action = QtWidgets.QAction("delete item", self)

        if self.permission != "admin":
            return
        self.table_view.customContextMenuRequested[QtCore.QPoint].connect(self.table_view_menu)
        self.add_item_action.triggered.connect(self.add_item_window)
        self.edit_item_action.triggered.connect(self.edit_item_window)
        self.delete_item_action.triggered.connect(self.delete_item)

        self.ad.accepted.connect(self.add_item)

    def table_view_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addActions([self.add_item_action, self.edit_item_action, self.delete_item_action])
        context_menu.exec_(self.table_view.mapToGlobal(point))

    def add_item_window(self):
        self.ad.exec_()
    
    def edit_item_window(self):
        current_item = self.table_view.currentItem()
        
        if not current_item:
            return

        label = current_item.data(self.label_role)
        imageOverlayLabel = current_item.data(self.image_label_role)
        image = current_item.data(self.image_role)
        sourceType = current_item.data(self.sourcetype_role)
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
        label = self.ad.label_line.text()
        if self.ad.python_radio_btn.isChecked():
            sourcetype = "python"
        if self.ad.mel_radio_btn.isChecked():
            sourcetype = "mel"
        overlay_label = self.ad.overlay_label_line.text()
        if self.ad.image_line.text():
            image = self.ad.image_line.text()
        else:
            if sourcetype == "python":
                image = self.python_icon
            else:
                image = self.mel_icon
        command = self.ad.command_text.toPlainText()
        double_click_command = self.ad.double_click_command_text.toPlainText()
        annotation = self.ad.annotation_text.toPlainText()

        item = QtWidgets.QListWidgetItem()
        item.setData(self.label_role, label)
        item.setData(self.image_label_role, overlay_label)
        item.setData(self.command_role, command)
        item.setData(self.double_command_role, double_click_command)
        item.setData(self.sourcetype_role, sourcetype)
        item.setData(self.image_role, image)
        item.setData(self.annotation_role, annotation)
        item.setIcon(QtGui.QPixmap(":{0}".format(image)))

        self.table_view.addItem(item)
    
    def edit_item(self):
        print "TODO"

    def delete_item(self):
        print "TODO"

    def add_shelf_button(self, item):
        label = item.data(self.label_role)
        imageOverlayLabel = item.data(self.image_label_role)
        image = item.data(self.image_role)
        sourceType = item.data(self.sourcetype_role)
        command = item.data(self.command_role)
        doubleClickCommand = item.data(self.double_command_role)
        annotation = item.data(self.annotation_role)

        current_tab = pm.tabLayout("ShelfLayout", query=True, selectTab=True)

        pm.shelfButton(parent=current_tab,
                        image=image,
                        command=command, 
                        doubleClickCommand=doubleClickCommand,
                        label=label,
                        imageOverlayLabel=imageOverlayLabel,
                        sourceType=sourceType,
                        annotation=annotation)

def run_asi(permission):
    # ui_name = AsiMayaUI.ui_name
    # if pm.window(ui_name, query=True, exists=True):
    #     pm.deleteUI(ui_name)
    ui = AsiMayaUI(permission=permission, parent=QtWidgets.QApplication.activeWindow())
    ui.show()


