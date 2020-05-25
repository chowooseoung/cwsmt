from PySide2 import QtWidgets


class ShelfDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ShelfDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        pass

    def sizeHint(self, option, index):
        pass
