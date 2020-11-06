from PySide2 import QtWidgets, QtCore, QtGui


class TestView(QtWidgets.QTableView):
    
    custom_clicked = QtCore.Signal(QtCore.QModelIndex)
    custom_double_clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(TestView, self).__init__(parent=parent)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_number = 0

    def mousePressEvent(self, event):
        super(TestView, self).mousePressEvent(event)
        print dir(event.)
        self.click_number += 1
        if not self.timer.isActive():
            self.timer.start()
        self.index1 = self.indexAt(event.pos())

    def mouseDoubleClickEvent(self, event):
        super(TestView, self).mouseDoubleClickEvent(event)
        self.click_number += 1
        self.index2 = self.indexAt(event.pos())

    def timeout(self):
        if self.click_number == 1:
            self.custom_clicked.emit(self.index1)
        elif (self.click_number == 2) & (self.index1 == self.index2):
            self.custom_double_clicked.emit(self.index1)
        self.click_number = 0


def click_command(index):
    print "click", index

def double_click_command(index):
    print "double", index

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tableView = TestView()
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData("test", QtCore.Qt.DisplayRole)
    model.setItem(0, item)
    tableView.setModel(model)
    tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tableView.custom_clicked[QtCore.QModelIndex].connect(click_command)
    tableView.custom_double_clicked[QtCore.QModelIndex].connect(double_click_command)
    tableView.show()
    sys.exit(app.exec_())