import sys
sys.path.append('D:\\maya\\scripts')

from PySide2 import QtWidgets, QtCore, QtGui
from common.gui.uiloader import UiLoader

import json
import os


class ShelfItem(QtGui.QStandardItem):

    @property
    def widget(self):
        return self.__widget

    @widget.setter
    def widget(self, w):
        self.__widget = w

    def __init__(self, name, runCode, toolTip, icon, label, widget):
        super(ShelfItem, self).__init__()

        self.__name = name
        self.__runCode = runCode
        self.__toolTip = toolTip
        self.__icon = icon
        self.__label = label
        self.widget = widget

    def set_data(self):
        pass

class ShelfModel(QtGui.QStandardItemModel):

    def __init__(self):
        super(ShelfModel, self).__init__()


class ShelfDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ShelfDelegate, self).__init__(parent)

        # self.preferenceWidget = CustomFrame()

    def paint(self, painter, option, index):
        if index.row() == 0:
            print 'a'
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        return QtCore.QSize(32, 32)



if __name__ == "__main__":
    """ Run the application. """
    from PySide2.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                                   QAbstractItemView)
    
    app = QApplication(sys.argv)

    print(sys.path)

    sys.exit(app.exec_())
