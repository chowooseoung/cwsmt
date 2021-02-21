# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtCompat
from coreui import SiTableView, SiModel, SiProxyModel, SiTableDelegate
from mworkspacecontrol import MWorkspaceControl
from functools import partial

import pymel.core as pm
import json
import os


class SiMayaTableView(SiTableView):

    si_clicked = QtCore.Signal(QtCore.QModelIndex)
    si_double_clicked = QtCore.Signal(QtCore.QModelIndex)
    si_shelf_clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(SiMayaTableView, self).__init__(parent=parent)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_number = 0
        self.index1 = None
        self.index2 = None

    def mousePressEvent(self, event):
        super(SiMayaTableView, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.index1 = self.indexAt(event.pos())
            if self.index1.isValid():
                if event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                    self.si_shelf_clicked.emit(self.index1)
                    return
            self.click_number += 1
            if not self.timer.isActive():
                self.timer.start()

    def mouseDoubleClickEvent(self, event):
        super(SiMayaTableView, self).mouseDoubleClickEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            if self.timer.isActive():
                self.click_number += 1
                self.index2 = self.indexAt(event.pos())
        
    def timeout(self):
        if self.click_number == 1:
            self.si_clicked.emit(self.index1)
        elif (self.click_number == 2) & (self.index1 == self.index2):
            self.si_double_clicked.emit(self.index1)
        self.click_number = 0


class SiMaya(QtWidgets.QMainWindow):
    
    __permission = None
    ui_admin_instance = None
    ui_guest_instance = None

    python_icon = ":/pythonFamily.png"
    mel_icon = ":/commandButton.png"

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
            self.workspace_control_instance.create("Scripts Interface", self, ui_script=self.get_ui_script(permission=permission))

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)

    @property
    def permission(self):
        return self.__permission
    
    @permission.setter
    def permission(self, p):
        self.__permission = p

    def __init__(self, permission="guest", parent=None):
        super(SiMaya, self).__init__(parent=parent)
        self.permission = permission

        self.setObjectName("{0}{1}".format(self.__class__.__name__, self.permission))
        self.create_widgets()
        self.create_connections()
        self.load_json()
        self.create_workspace_control(permission=self.permission)
        self.get_json()

    def create_widgets(self):
        self.ad = QtWidgets.QDialog()
        self.ed = QtWidgets.QDialog()
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "main.ui"), self)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "maya_item.ui"), self.ad)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui", "maya_item.ui"), self.ed)

        self.table_view = SiMayaTableView()
        self.view_layout.addWidget(self.table_view)
        self.proxy_model = SiProxyModel()
        self.proxy_model.setSourceModel(SiModel())
        self.table_view.setModel(self.proxy_model)
        self.table_view.setItemDelegate(SiTableDelegate())
        self.table_view.horizontalHeader().hideSection(4)
        self.table_view.horizontalHeader().hideSection(5)
        # self.table_view.setColumnWidth(1, 60)
        
        self.tags_view.hide()

        self.json_list_action_group = QtWidgets.QActionGroup(self)
        
        self.tags_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.table_view.horizontalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.icon_column_hide = QtWidgets.QAction("icon", self)
        self.icon_column_hide.setCheckable(True)
        self.label_column_hide = QtWidgets.QAction("label", self)
        self.label_column_hide.setCheckable(True)
        self.author_column_hide = QtWidgets.QAction("author", self)
        self.author_column_hide.setCheckable(True)
        self.tags_column_hide = QtWidgets.QAction("tags", self)
        self.tags_column_hide.setCheckable(True)


        if self.permission == "guest":  
            self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.file_menu.addSeparator()
            self.refresh_btn = QtWidgets.QAction("Refresh", self)
            self.file_menu.addAction(self.refresh_btn)
            return
        self.add_item_action = QtWidgets.QAction("add item" , self)
        self.edit_item_action = QtWidgets.QAction("edit item", self)
        self.delete_item_action = QtWidgets.QAction("delete item", self)
        
        self.save_action_btn = QtWidgets.QAction("Save", self)
        self.create_json_btn = QtWidgets.QAction("Create", self)
        self.delete_json_btn = QtWidgets.QAction("Delete", self)
        self.file_menu.addAction(self.save_action_btn)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.create_json_btn)
        self.file_menu.addAction(self.delete_json_btn)

        self.btn_layout = QtWidgets.QHBoxLayout()
        self.centralwidget.layout().addLayout(self.btn_layout)

        self.up_item_btn = QtWidgets.QPushButton("up")
        self.down_item_btn = QtWidgets.QPushButton("down")
        self.btn_layout.addWidget(self.up_item_btn)
        self.btn_layout.addWidget(self.down_item_btn)

    def create_connections(self):
        self.load_action_btn.triggered.connect(self.load_json)
        self.search_line.textChanged.connect(self.proxy_model.setLineFilter)
        self.table_view.model().sourceModel().dataChanged.connect(self.setup_tags_view)
        self.tags_view.cellChanged.connect(self.tags_filter)
        self.json_list_action_group.triggered.connect(self.load_json)
        self.tags_view_action.triggered.connect(self.view_mode)
        self.table_view.horizontalHeader().customContextMenuRequested.connect(self.table_view_header_menu)
        self.icon_column_hide.triggered.connect(partial(self.hide_column))
        self.label_column_hide.triggered.connect(partial(self.hide_column))
        self.author_column_hide.triggered.connect(partial(self.hide_column))
        self.tags_column_hide.triggered.connect(partial(self.hide_column))

        if self.permission == "guest":
            self.table_view.si_clicked[QtCore.QModelIndex].connect(partial(self.run_command, clickType="command"))
            self.table_view.si_double_clicked[QtCore.QModelIndex].connect(partial(self.run_command, clickType="doubleCommand"))
            self.table_view.si_shelf_clicked[QtCore.QModelIndex].connect(self.add_shelf_button)
            self.refresh_btn.triggered.connect(self.get_json)
            return
        self.ad.accepted.connect(self.add_item)
        self.ed.accepted.connect(self.edit_item)
        self.save_action_btn.triggered.connect(self.save_json)
        self.table_view.customContextMenuRequested[QtCore.QPoint].connect(self.table_view_menu)
        self.add_item_action.triggered.connect(self.add_item_window)
        self.edit_item_action.triggered.connect(self.edit_item_window)
        self.delete_item_action.triggered.connect(self.delete_item)
        self.create_json_btn.triggered.connect(self.create_json)
        self.delete_json_btn.triggered.connect(self.delete_json)
        self.up_item_btn.clicked.connect(self.up_item)
        self.down_item_btn.clicked.connect(self.down_item)
    
    def view_mode(self):
        if self.tags_view_action.isChecked(): 
            self.tags_view.show()
        else: 
            self.tags_view.hide()

    def hide_column(self):
        if self.icon_column_hide.isChecked():
            self.table_view.horizontalHeader().hideSection(0)
        else:
            self.table_view.horizontalHeader().showSection(0)

        if self.label_column_hide.isChecked():
            self.table_view.horizontalHeader().hideSection(1)
        else:
            self.table_view.horizontalHeader().showSection(1)
        
        if self.author_column_hide.isChecked():
            self.table_view.horizontalHeader().hideSection(2)
        else:
            self.table_view.horizontalHeader().showSection(2)
        
        if self.tags_column_hide.isChecked():
            self.table_view.horizontalHeader().hideSection(3)
        else:
            self.table_view.horizontalHeader().showSection(3)
        
    def table_view_header_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.setTitle("Hide Column")
        context_menu.addActions([self.icon_column_hide, self.label_column_hide, self.author_column_hide, self.tags_column_hide])
        context_menu.exec_(self.table_view.mapToGlobal(point))

    def table_view_menu(self, point):
        header_point = QtCore.QPoint(self.table_view.verticalHeader().width(), self.table_view.horizontalHeader().height())
        context_menu = QtWidgets.QMenu()
        context_menu.addActions([self.add_item_action, self.edit_item_action, self.delete_item_action])
        context_menu.exec_(self.table_view.mapToGlobal(point + header_point))

    def setup_tags_view(self):
        self.tags_view.clearContents()
        
        colors = self.table_view.model().sourceModel().colors
        self.tags_view.setRowCount(len(colors))
        self.tags_view.setColumnCount(2)
        for index, key in enumerate(sorted(colors)):
            check_cell = QtWidgets.QWidget()
            check_layout = QtWidgets.QHBoxLayout(check_cell)
            check_layout.setAlignment(QtCore.Qt.AlignCenter)
            check_layout.setContentsMargins(0, 0, 0, 0)
            checkbox = QtWidgets.QCheckBox()
            checkbox.stateChanged[int].connect(partial(self.check_tags, txt=key))
            check_layout.addWidget(checkbox)

            tag_cell = QtWidgets.QWidget()
            tag_layout = QtWidgets.QHBoxLayout(tag_cell)
            tag_layout.setAlignment(QtCore.Qt.AlignLeft)
            tag_layout.setContentsMargins(4, 4, 4, 4)
            frame = QtWidgets.QFrame()
            frame.setStyleSheet("QFrame {{\nbackground-color: hsva({0}, 100, 222, 255);\nborder-radius: 4px;\n}}".format(colors[key]))
            frame.setFixedHeight(20)
            label = QtWidgets.QLabel(key)
            label.setStyleSheet("QLabel {\ncolor: #000000;}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            frame_layout = QtWidgets.QHBoxLayout(frame)
            frame_layout.addWidget(label)
            frame_layout.setContentsMargins(2, 0, 2, 2)
            tag_layout.addWidget(frame)
            self.tags_view.setCellWidget(index, 0, check_cell)
            self.tags_view.setCellWidget(index, 1, tag_cell)

    def check_tags(self, isChecked, txt):
        if bool(isChecked) == True:
            self.proxy_model.setTagsFilter(txt)
        else:
            self.proxy_model.clearTagsFilter(txt)

    def tags_filter(self, row, column):
        item = self.tags_view.item(row, column)
        lastState = item.data(QtCore.Qt.UserRole)
        currentState = item.checkState()
        
        if currentState != lastState:
            if currentState == QtCore.Qt.Checked:
                self.proxy_model.setTagsFilter(self.tags_view.item(row, 1).data(QtCore.Qt.DisplayRole))
            else:
                self.proxy_model.clearTagsFilter(self.tags_view.item(row, 1).data(QtCore.Qt.DisplayRole))
            item.setData(QtCore.Qt.UserRole, currentState)

    def add_item_window(self):
        self.ad.author_line.clear()
        self.ad.label_line.clear()
        self.ad.overlay_label_line.clear()
        self.ad.image_line.clear()
        self.ad.python_radio_btn.setChecked(True)
        self.ad.command_text.clear()
        self.ad.double_click_command_text.clear()
        description = "{:<9} : ".format("Requested")
        description += "\n"
        description += "{:<9} : ".format("PurPose")
        self.ad.annotation_text.setText(description)
        self.ad.author_line.setFocus()
        self.ad.exec_()
    
    def edit_item_window(self):
        self.ed.setWindowTitle("edit item")
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        current_index = self.table_view.currentIndex()
        index = proxy_model.mapToSource(current_index)
        if not index.isValid():
            return
        row = index.row()

        icon = model.data(index=model.index(row, 0), role=QtCore.Qt.DisplayRole)
        label = model.data(index=model.index(row, 1), role=QtCore.Qt.DisplayRole)
        author = model.data(index=model.index(row, 2), role=QtCore.Qt.DisplayRole)
        annotation = model.data(index=model.index(row, 4), role=QtCore.Qt.DisplayRole)
        meta = model.data(index=model.index(row, 5), role=QtCore.Qt.DisplayRole)
        imageoverlay = meta["overlayLabel"]
        source_type = meta["sourceType"]
        command = meta["command"]
        double_command = meta["doubleCommand"]

        if source_type == "python":
            self.ed.python_radio_btn.setChecked(True)
        else:
            self.ed.mel_radio_btn.setChecked(True)
        self.ed.image_line.setText(icon)
        self.ed.label_line.setText(label)
        self.ed.author_line.setText(author)
        self.ed.overlay_label_line.setText(imageoverlay)
        self.ed.command_text.setPlainText(command)
        self.ed.double_click_command_text.setPlainText(double_command)
        self.ed.annotation_text.setPlainText(annotation)
        self.ed.author_line.setFocus()
        self.ed.exec_()
    
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
        data.append(image)
        data.append(label)
        data.append(author)
        data.append(list())
        data.append(annotation)
        meta = {   
            u"sourceType" : source_type,
            u"command" : command,
            u"doubleCommand" : double_click_command,
            u"overlayLabel" : overlay_label
        }
        data.append(meta)
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        model.insertRows(position=model.rowCount(), data=data)

    def edit_item(self):
        icon = self.ed.image_line.text()
        label = self.ed.label_line.text()
        author = self.ed.author_line.text()
        if self.ed.mel_radio_btn.isChecked():
            source_type = "mel"
        elif self.ed.python_radio_btn.isChecked():
            source_type = "python"
        overlay_label = self.ed.overlay_label_line.text()
        command = self.ed.command_text.toPlainText()
        double_click_command = self.ed.double_click_command_text.toPlainText()
        annotation = self.ed.annotation_text.toPlainText()
        meta = {   
            u"sourceType" : source_type,
            u"command" : command,
            u"doubleCommand" : double_click_command,
            u"overlayLabel" : overlay_label
        }

        proxy_model = self.table_view.model()
        proxy_index = self.table_view.currentIndex()
        index = proxy_model.mapToSource(proxy_index)
        model = proxy_model.sourceModel()
        row = index.row()
        model.setData(index=model.index(row, 0), value=icon, role=QtCore.Qt.EditRole)
        model.setData(index=model.index(row, 1), value=label, role=QtCore.Qt.EditRole)
        model.setData(index=model.index(row, 2), value=author, role=QtCore.Qt.EditRole)
        model.setData(index=model.index(row, 4), value=annotation, role=QtCore.Qt.EditRole)
        model.setData(index=model.index(row, 5), value=meta, role=QtCore.Qt.EditRole)

    def delete_item(self):
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        proxy_index = self.table_view.currentIndex()
        if not proxy_index.isValid():
            return 
        source_index = proxy_model.mapToSource(proxy_index)
        pos = source_index.row()
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

    def up_item(self):
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        proxy_index = self.table_view.currentIndex()
        if not proxy_index.isValid():
            return 
        source_index = proxy_model.mapToSource(proxy_index)

        data = model.data(source_index, QtCore.Qt.UserRole+1)
        if source_index.row() == 0:
            row = 0
        else:
            row = source_index.row()-1
        model.removeRows(source_index.row())
        model.insertRows(row, data=data)

        self.table_view.selectRow(row)

    def down_item(self):
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        proxy_index = self.table_view.currentIndex()
        if not proxy_index.isValid():
            return 
        source_index = proxy_model.mapToSource(proxy_index)

        data = model.data(source_index, QtCore.Qt.UserRole+1)
        count = model.rowCount()
        if source_index.row() == count-1:
            row = source_index.row()
        else:
            row = source_index.row()+1
        model.removeRows(source_index.row())
        model.insertRows(row, data=data)

        self.table_view.selectRow(row)

    def get_json(self):
        orig_checked = self.json_list_action_group.checkedAction()
        for action in self.json_list_action_group.actions():
            self.file_menu.removeAction(action)
            self.json_list_action_group.removeAction(action)
        json_list = [x for x in os.listdir(os.path.join(os.path.dirname(__file__), "json")) if x.endswith("json")]
        json_list = [x for x in json_list if "Colors" not in x]

        for json in json_list:
            act = QtWidgets.QAction(json.split(".")[0], self)
            act.setCheckable(True)
            self.json_list_action_group.addAction(act)
            self.file_menu.addAction(act)
        if orig_checked:    
            for act in self.json_list_action_group.actions():
                if act.text() == orig_checked.text():
                    act.setChecked(True)
        if self.json_list_action_group.actions():
            if not self.json_list_action_group.checkedAction():
                self.json_list_action_group.actions()[0].setChecked(True)
        self.load_json()

    def create_json(self):
        directory = os.path.join(os.path.dirname(__file__), "json")
        json_list = [x for x in os.listdir(os.path.join(os.path.dirname(__file__), "json")) if ".delete" not in x]
        
        input_dialog = QtWidgets.QInputDialog()
        txt, result = input_dialog.getText(self, "Get name", "json name", QtWidgets.QLineEdit.Normal, "")
        check = [x for x in json_list if x.split(".")[0] == txt]
        if result and (not check):
            with open(os.path.join(directory, "{0}.json".format(txt)), "w") as f: 
                json.dump(dict(), f, indent=4)
            with open(os.path.join(directory, "{0}Colors.json".format(txt)), "w") as f: 
                json.dump(dict(), f, indent=4)
        self.get_json()

    def save_json(self):
        if self.json_list_action_group.checkedAction():
            name = self.json_list_action_group.checkedAction().text()
        else:
            return

        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        with open(os.path.join(os.path.dirname(__file__), "json", "{0}Colors.json".format(name)), "w") as f: 
            json.dump(model.colors, f, indent=4)
        
        data = dict()
        temp = model.scripts
        for index in range(len(temp)):
            data[unicode(index)] = {
                u"Icon":temp[index][0], 
                u"Label":temp[index][1], 
                u"Author":temp[index][2], 
                u"Tags":temp[index][3], 
                u"Annotation":temp[index][4], 
                u"Meta":temp[index][5]
            }
        with open(os.path.join(os.path.dirname(__file__), "json", "{0}.json".format(name)), "w") as f: 
            json.dump(data, f, indent=4)

    def load_json(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "json")):
            os.mkdir(os.path.join(os.path.dirname(__file__), "json"))

        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        model.reset()

        if self.json_list_action_group.checkedAction():
            name = self.json_list_action_group.checkedAction().text()
        else:
            return
        with open(os.path.join(os.path.dirname(__file__), "json", "{0}Colors.json".format(name))) as f: 
            colors = json.load(f)
        with open(os.path.join(os.path.dirname(__file__), "json", "{0}.json".format(name))) as f: 
            scripts = json.load(f)
        model.colors = colors 

        for index in sorted([int(x) for x in scripts]):
            data = list()
            data.append(scripts[str(index)]["Icon"])
            data.append(scripts[str(index)]["Label"])
            data.append(scripts[str(index)]["Author"])
            data.append(scripts[str(index)]["Tags"])
            data.append(scripts[str(index)]["Annotation"])
            data.append(scripts[str(index)]["Meta"])
            model.insertRows(position=int(index), data=data)
        self.proxy_model.clearTagsFilters()

    def delete_json(self):
        name = self.json_list_action_group.checkedAction().text()
        colors = os.path.join(os.path.dirname(__file__), "json", "{0}Colors.json".format(name))
        scripts = os.path.join(os.path.dirname(__file__), "json", "{0}.json".format(name))

        num = 0
        while True:
            if os.path.basename(scripts)+".delete"+str(num) not in os.listdir(os.path.join(os.path.dirname(__file__), "json")):
                rename_scripts = scripts+".delete"+str(num)
                rename_colors = colors+".delete"+str(num)
                break
            num += 1
        os.rename(colors, rename_colors)
        os.rename(scripts, rename_scripts)
        self.get_json()

    def run_command(self, index, clickType):
        if not index.isValid():
            return
        proxy_model = self.table_view.model()
        index = proxy_model.mapToSource(index)
        model = proxy_model.sourceModel()
        meta_data = model.data(index=model.index(index.row(), 5), role=QtCore.Qt.DisplayRole)
        
        source_type = meta_data["sourceType"]
        command = meta_data[clickType]
        check = set()
        for c in command:
            check.add(c)
        if check.issubset(set(["\n", " ", "\t", ""])):
            return
        if source_type == "python":
            pm.undoInfo(openChunk=True)
            pm.evalDeferred(command)
            pm.undoInfo(closeChunk=True)
        else:
            pm.undoInfo(openChunk=True)
            pm.mel.eval(command)
            pm.undoInfo(closeChunk=True)
        
    def add_shelf_button(self, index):
        if not index.isValid():
            return
        proxy_model = self.table_view.model()
        model = proxy_model.sourceModel()
        index = proxy_model.mapToSource(index)

        icon = model.data(index=model.index(index.row(), 0), role=QtCore.Qt.DisplayRole)
        label = model.data(index=model.index(index.row(), 1), role=QtCore.Qt.DisplayRole)
        annotation = model.data(index=model.index(index.row(), 4), role=QtCore.Qt.DisplayRole)
        meta = model.data(index=model.index(index.row(), 5), role=QtCore.Qt.DisplayRole)
        imageoverlay_label = meta["overlayLabel"]
        source_type = meta["sourceType"]
        command = meta["command"]
        double_command = meta["doubleCommand"]

        current_tab = pm.tabLayout("ShelfLayout", query=True, selectTab=True)

        pm.shelfButton(parent=current_tab,
                        image=icon,
                        command=command, 
                        doubleClickCommand=double_command,
                        label=label,
                        imageOverlayLabel=imageoverlay_label,
                        sourceType=source_type,
                        annotation=annotation)
                
    def showEvent(self, event):
        super(SiMaya, self).showEvent(event)
        self.load_json()