import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QColor, QKeyEvent
from PySide2.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QApplication


class MyDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        return CustomEditor(parent)

    def updateEditorGeometry(self, editor, option, index):
        # adjust position if close to border
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        (text, bgColor) = ('', '')
        data = index.data()
        print data
        if type(data) == list and len(data) > 1:
            (text, bgColor) = data
        painter.setBrush(QColor(bgColor))
        painter.drawRect(option.rect)
        painter.setPen(QColor(100, 255, 255))
        painter.drawText(option.rect, QtCore.Qt.AlignCenter, text)

    def setEditorData(self, editor, index):
        data = index.data()
        if type(data) == tuple and len(data) > 1:
            (text, bgColor) = index.data()
            editor.edit1.setText(text)
            editor.edit2.setText(bgColor)

    def setModelData(self, editor, model, index):
        model.setData(index, (editor.edit1.text(), editor.edit2.text()))


class CustomEditor(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.edit1 = QLineEdit()
        self.edit2 = QLineEdit()
        self.button = QPushButton("close")
        layout = QVBoxLayout()
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.saveAndClose)
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(64, 128))

    def saveAndClose(self):
        QApplication.postEvent(self, QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier))


class Model(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.colorData = [('abc', '#173f5f'),
                          ('def', '#20639b'),
                          ('ghi', '#3caea3'),
                          ('red', '#ff0000'),
                          ('mno', '#ed553b')]

    def rowCount(self, parent):
        return len(self.colorData)

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.colorData[index.row()]
        return None

    def setData(self, index, value, role=None):
        if role != Qt.EditRole:
            self.colorData[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable


class TableView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        tableModel = Model()
        tableView = QtWidgets.QTableView()
        tableView.setModel(tableModel)
        mydelegate = MyDelegate(self)
        tableView.setItemDelegateForColumn(1, mydelegate)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(tableView)
        self.setLayout(hbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tableView = TableView()
    tableView.setMinimumSize(QSize(400, 360))
    tableView.show()
    sys.exit(app.exec_())