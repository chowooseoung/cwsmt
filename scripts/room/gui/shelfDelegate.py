from PySide2 import QtWidgets
from common.gui.uiloader as UiLoader

import os


class ShelfDelegate(QtWidgets.QStyledItemDelegate):

    PREFERENCEUI = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'preferenceItem.ui'))
    PARENTUI = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'parentItem.ui'))

    def __init__(self, parent=None):
        super(ShelfDelegate, self).__init__(parent)

        self.preferenceWidget = QtWidgets.QWidget()
        UiLoader().loadUi(uifile=self.PREFERENCEUI, self.preferenceWidget)

        self.parentWidget = QtWidgets.QWidget()
        UiLoader().loadUi(uifile=self.PARENTUI, self.parentWidget)

    def paint(self, painter, option, index):
        pass

    def sizeHint(self, option, index):
        pass
