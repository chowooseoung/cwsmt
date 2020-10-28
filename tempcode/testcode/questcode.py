from PySide2 import QtWidgets, QtCore, QtGui


class TestDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(TestDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        wid = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(wid)
        btn = QtWidgets.QPushButton()
        layout.addWidget(btn)
        wid.setAutoFillBackground(True)
        painter.save()
        painter.translate(option.rect.topLeft())
        wid.resize(option.rect.size())
        wid.render(painter, QtCore.QPoint(0, 0))
        painter.restore()
    
    def createEditor(self, parent, option, index):
        wid = QtWidgets.QWidget(parent=parent)
        layout = QtWidgets.QHBoxLayout(wid)
        btn = QtWidgets.QPushButton()
        layout.addWidget(btn)
        wid.setAutoFillBackground(True)
        wid.setContentsMargins(2, 2, 2, 2)
        return wid

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    table = QtWidgets.QTableWidget(4,4)
    table.setItemDelegate(TestDelegate())
    table.show()
    sys.exit(app.exec_())