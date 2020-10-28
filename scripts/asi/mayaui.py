from Qt import QtWidgets, QtCore, QtGui, QtCompat
from functools import partial

import pymel.core as pm
import json
import os
import asi as coreui


class AsiMaya(coreui.AsiCoreUI):

    __ui_name = "ArtistScriptsInterfaceMaya"
    python_icon = "pythonFamily.png"
    mel_icon = "commandButton.png"
    
    @property
    def ui_name(self):
        return self.__ui_name

    def __init__(self, user, tool, parent):
        super(AsiMaya, self).__init__(user=user, tool=tool, parent=parent)

        self.setObjectName(self.ui_name)

    def create_ui(self):
        super(AsiMaya, self).create_ui()

        self.ad = QtWidgets.QDialog()
        QtCompat.loadUi(os.path.join(os.path.dirname(__file__), "ui/add_item.ui"), self.ad)

        self.add_item_action = QtWidgets.QAction("add item" , self)
        self.edit_item_action = QtWidgets.QAction("edit item", self)
        self.delete_item_action = QtWidgets.QAction("delete item", self)

    def create_connections(self):
        super(AsiMaya, self).create_connections()

        self.item_view.itemDoubleClicked.connect(self.add_shelf_button)
        if self.user != "admin":
            return
        self.item_view.customContextMenuRequested[QtCore.QPoint].connect(self.item_view_menu)
        # self.tags_view.customContextMenuRequested[QtCore.QPoint].connect(self.tags_view_menu)

        self.add_item_action.triggered.connect(self.add_item_window)
        self.edit_item_action.triggered.connect(self.edit_item_window)
        self.delete_item_action.triggered.connect(self.delete_item)

        self.ad.accepted.connect(self.add_item)

    def item_view_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addActions([self.add_item_action, self.edit_item_action, self.delete_item_action])
        context_menu.exec_(self.item_view.mapToGlobal(point))

    def add_item_window(self):
        self.ad.exec_()
    
    def edit_item_window(self):
        current_item = self.item_view.currentItem()
        
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

        self.item_view.addItem(item)
    
    def edit_item(self):
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

def run_asi(user):
    ui_name = AsiMaya.ui_name
    if pm.window(ui_name, query=True, exists=True):
        pm.deleteUI(ui_name)
    ui = AsiMaya(user=user, parent=QtWidgets.QApplications.activeWindow())
    ui.show()


if __name__ == "__main__":
    import asi.maya as asimaya
    reload(asimaya)
    asimaya.run_asi(user="admin")