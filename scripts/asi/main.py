# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from functools import partial
from asi import mayacommand

import os


class AsiUI(QtWidgets.QDialog):

    ui_name = "ArtistScriptsInterface"
    python_icon = ""
    mel_icon = ""

    def __init__(self, parent, user):
        super(AsiUI, self).__init__(parent=parent)

        self.user = user
        self.ad = QtWidgets.Qdialog()
        self.create_ui()
        self.create_connections()
    
    def create_ui(self):
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui/main.ui"), self)
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui/add_item.ui"), self.ad)
        self.setObjectName(self.ui_name)

        self.add_item_action = QtWidgets.QAction("add item" , self)
        self.edit_item_action = QtWidgets.QAction("edit item", self)
        self.delete_item_action = QtWidgets.QAction("delete item", self)

    def create_connections(self):
        self.item_view.itemDoubleClicked.connect(mayacommand.add_shelf_button)
        if self.user == "TD":
            self.item_view.customContextMenuRequested[QtCore.QPoint].connect(self.item_view_menu)

        self.add_item_action.triggered.connect(self.add_item_window)
        self.ad.accepted.connect(self.add_item)
    
    def item_view_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addActions(self.add_item_action)
        context_menu.addActions(self.edit_item_action)
        context_menu.addActions(self.delete_item_action)
        context_menu.exec_(self.itemview.mapToGlobal(point))

    def add_item_window(self):
        self.ad.exec_()
    
    def edit_item_window(self):
        print "TODO"
    
    def add_item(self):
        label = self.ad.label_line.text()
        if self.ad.python_radio_btn.isChecked():
            source_type = "python"
        else:
            source_type = "mel"
        overlay_label = self.ad.overlay_label_line.text()
        if self.ad.icon_path_line.text():
            icon_path = self.icon_path_line.text()
        else:
            if source_type == "python":
                icon_path = self.python_icon
            else:
                icon_path = self.mel_icon
        command = self.ad.command_text.toPlainText()
        double_click_command = self.ad.double_click_command_text.toPlainText()
        annotation = self.ad.tooltip_text.toPlainText()

        item = QtWidgets.QListWidgetItem()
        item.setData(self.label_role, label)
        item.setData(self.image_label_role, overlay_label)
        item.setData(self.command_role, command)
        item.setData(self.double_command_role, double_click_command)
        item.setData(self.sourcetype_role, source_type)
        item.setData(self.icon_role, icon_path)
        item.setData(QtGui.QPixmap(":{0}".format(icon_path)))

        self.item_view.addItem(item)
    
    def delete_item(self):
        print "TODO"
    
    def save_json(self):
        print "TODO"

    def load_json(self):
        print "TODO"
    
    def refresh(self):
        print "TODO"
    
    def add_tags(self):
        print "TODO"
    
    @classmethod
    def display(cls, user):
        if pm.window(cls.ui_name, query=True, exists=True)
            pm.deleteUI(cls.ui_name)
        ui = cls(parent=QtWidgets.QApplication.activeWidnow(), user=user)
        ui.show()
    

if __name__ == "__main__":
    import asi.main as asi
    reload(asi)
    asi.AsiUI.display(user="TD")