# -*- coding:utf-8 -*-

from PySide2 import QtWidgets, QtCore, QtGui


class Tags(QtWidgets.QLineEdit):

    def __init__(self):
        super(Tags, self).__init__()

class Tag(QtWidgets.QWidget):

    __name = None
    __color = None

    @property
    def name(self):
        return self.__name
    
    @property
    def color(self):
        return self.__color

    @name.setter
    def name(self, n):
        self.__name = n

    @color.setter
    def color(self, c):
        self.__color = c

    def __init__(self, name, color):
        super(Tag, self).__init__()
        
        self.name = name
        self.color = color
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        r, g, b, a = self.color
        self.setStyleSheet("QWidget#{tag} {{\nbackground-color: hsva({0}, {1}, {2}, {3});\nborder-radius: 10px;\n}}".format(r, g, b, a, tag="{0}Tag".format(self.name)))
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        
    def create_widgets(self):
        self.label = QtWidgets.QLabel(self.name)
        self.x_button = QtWidgets.QPushButton()

    def create_layout(self):
        tag_layout = QtWidgets.QHBoxLayout(self)
        tag_layout.addWidget(self.label)
        tag_layout.addWidget(self.x_button)
        tag_layout.setContentsMargins(2, 2, 2, 2)

    def create_connections(self):
        self.x_button.clicked.connect(self.delete_tag)

    def button_visibility(self, switch):
        if switch is True:
            self.x_button.show()
        elif switch is False: 
            self.x_button.hide()
            self.x_button.setParent(None)

    def delete_tag(self):
        self.deleteLater()
    
    def sizeHint(self):
        return self.label.sizeHint() + self.x_button.sizeHint()

    # def paint(self, painter, rect, palette, isEditable=False):

    #     painter.save() # 저장

    #     painter.setRenderHint(QtGui.QPainter.Antialiasing, True) # 안티엘리어싱 on
    #     painter.setPen(QtCore.Qt.NoPen) # 펜 off

    #     if isEditable:
    #         painter.setBrush(palette.highlight())
    #     else:
    #         painter.setBrush(palette.windowText())

    #     yOffset = (rect.height() - PAINTING_SCALE_FACTOR) / 2
    #     painter.translate(rect.x(), rect.y() + yOffset)
    #     painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)

    #     for i in range(self.maxStarCount):
    #         if i < self.starCount:
    #             painter.drawPolygon(self.starPolygon, Qt.WindingFill)
    #         elif isEditable:
    #             painter.drawPolygon(self.diamondPolygon, Qt.WindingFill)
    #         painter.translate(1.0, 0.0)

    #     painter.restore() # 되돌리기

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Create and populate the tableWidget
    tableWidget = QtWidgets.QTableWidget(1, 1)
    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | 
                                QtWidgets.QAbstractItemView.SelectedClicked)
    tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    tableWidget.setHorizontalHeaderLabels(["Title", "Genre", "Artist", "Rating"])

    tag1 = Tag(name="testTag", color=(155, 70, 255, 255))

    # tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(tag1))

    tableWidget.resizeColumnsToContents()
    tableWidget.resize(500, 300)
    tableWidget.show()
    
    print tag1.label.sizeHint()
    print tag1.x_button.sizeHint()
    sys.exit(app.exec_())
