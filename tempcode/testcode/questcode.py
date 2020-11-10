from PySide2 import QtCore, QtWidgets

LastStateRole = QtCore.Qt.UserRole

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tablewidget = QtWidgets.QTableWidget(4, 4)
        self.setCentralWidget(self.tablewidget)

        my_list = ["A", "B", "C", "D"]
        for row in range(len(my_list)):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            item.setData(LastStateRole, item.checkState())

            self.tablewidget.setItem(row, 0, item)

        self.tablewidget.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        item = self.tablewidget.item(row, column)
        lastState = item.data(LastStateRole)
        currentState = item.checkState()
        if currentState != lastState:
            print("changed: ")
            if currentState == QtCore.Qt.Checked:
                print("checked")
            else:
                print("unchecked")
            item.setData(LastStateRole, currentState)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())