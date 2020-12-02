from PySide2 import QtWidgets, QtGui, QtCore
import sys
class Delegate(QtWidgets.QStyledItemDelegate):
    def updateEditorGeometry(self, editor, option, index):
        super(Delegate, self).updateEditorGeometry(editor, option, index)
        geo = editor.geometry().adjusted(0, 4, 0, 0)
        editor.setGeometry(geo)

class ReorderList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ReorderList, self).__init__(parent)
        delegate = Delegate(self)
        self.setItemDelegate(delegate)
        self.dropIndicatorRect = QtCore.QRect()
        self.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove
        )
        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove
        )

    def add_btn(self, text='', index=-1):
        widget = QtWidgets.QWidget()
        if not text:
            text = 'item {0}'.format(self.count() + 1)
        btn = QtWidgets.QPushButton(text)

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(btn.sizeHint())

        if index < 0:
            self.addItem(item)
        else:
            self.insertItem(index, item)
        self.setItemWidget(item, btn)

    def dropEvent(self, event):
        drop_index = self.indexAt(event.pos()).row()
        self.add_btn(index=drop_index)
        self.dropIndicatorRect = QtCore.QRect()
        self.viewport().update()
        super(ReorderList, self).dropEvent(event)

    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        self.dropIndicatorRect = QtCore.QRect()
        self.viewport().update()
        super(ReorderList, self).dragLeaveEvent(event)

    def onClick(self):
        print self.sender().text()

    def dragMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            rect = self.visualRect(index)
            if self.dropIndicatorPosition() == QtWidgets.QAbstractItemView.OnItem:
                self.dropIndicatorRect = rect
            else:
                self.dropIndicatorRect = QtCore.QRect()
        else:
            self.dropIndicatorRect = QtCore.QRect()
        self.viewport().update()
        super(ReorderList, self).dragMoveEvent(event)

    def paintEvent(self, event):
        super(ReorderList, self).paintEvent(event)
        if not self.dropIndicatorRect.isNull() and self.showDropIndicator():
            painter = QtGui.QPainter(self.viewport())
            p = QtGui.QPen(painter.pen())
            p.setWidthF(1.5)
            painter.setPen(p)
            r = self.dropIndicatorRect
            painter.drawLine(r.topLeft(), r.topRight())

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = ReorderList()
    win.show()
    sys.exit(app.exec_())