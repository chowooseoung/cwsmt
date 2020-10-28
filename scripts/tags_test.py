from PySide2 import QtWidgets, QtCore, QtGui


class TestUI(QtWidgets.QWidget):

    def __init__(self, parent=None):    
        super(TestUI, self).__init__(parent=parent)
        l = QtWidgets.QHBoxLayout(self)
        self.item_view = QtWidgets.QTableWidget(4, 4)
        l.addWidget(self.item_view)
        self.item_view.setItemDelegate(TestDelegate(self.item_view))
        self.item_view.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | 
                                    QtWidgets.QAbstractItemView.SelectedClicked)
        self.item_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.item_view.setHorizontalHeaderLabels(["Title", "Genre", "Artist", "Rating"])
        self.refresh()

        self.item_view.resizeColumnsToContents()
        self.item_view.resize(500, 300)

    def refresh(self):
        self.item_view.clear()

        tag_item = QtWidgets.QTableWidgetItem()
        tag_item.setData(QtCore.Qt.UserRole, ["maya", "utils", "modeling"])
        self.item_view.setItem(0, 0, tag_item)

class TestDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, v):
        super(TestDelegate, self).__init__(v)

    def paint(self, painter, option, index):
        if index.column() == 0:
            if index.data(QtCore.Qt.UserRole):
                self.n = 0
                for name in index.data(QtCore.Qt.UserRole):
                    painter.save()
                    a = TestTag(name=name)
                    painter.translate(option.rect.topLeft())
                    a.render(painter, QtCore.QPoint(self.n, 0))
                    self.n += (a.sizeHint().width()+30)
                    painter.restore()
                    
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.fillRect(option.rect, painter.brush())
            
            # starRating.paint(painter, option.rect, option.palette)
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        if index.column() == 0:
            # starRating = StarRating(index.data())
            # return starRating.sizeHint()
            return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        else:
            return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)

class TestTag(QtWidgets.QWidget):
    
    __name = None

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, n):
        self.__name = n

    def __init__(self, name):
        super(TestTag, self).__init__()
        self.name = name
        
        self.create_widgets()
        self.create_layout()

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        
    def create_widgets(self):
        self.label = QtWidgets.QLabel(self.name)
        self.x_button = QtWidgets.QPushButton("x")

    def create_layout(self):
        tag_layout = QtWidgets.QHBoxLayout(self)
        tag_layout.addWidget(self.label)
        tag_layout.addWidget(self.x_button)

    def sizeHint(self):
        return self.label.sizeHint() + self.x_button.sizeHint()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    a = TestUI()
    a.show()
    sys.exit(app.exec_())