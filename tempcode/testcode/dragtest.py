from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
class DragTest(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(DragTest, self).__init__()

        cent = QtWidgets.QWidget()
        self.setCentralWidget(cent)

        layout = QtWidgets.QHBoxLayout(cent)
        self.color1_btn = QtWidgets.QPushButton(acceptDrops=True)
        self.color1_btn.clicked.connect(partial(self.color_btn_click, widget=self.color1_btn))
        self.color2_btn = QtWidgets.QPushButton(acceptDrops=True)
        self.color2_btn.clicked.connect(partial(self.color_btn_click, widget=self.color2_btn))
        layout.addWidget(self.color1_btn)
        layout.addWidget(self.color2_btn)
        self.color1_btn.installEventFilter(self)
        self.color2_btn.installEventFilter(self)
        self.color1_btn.color = self.color2_btn.color = None

        self.btn1 = QtWidgets.QPushButton()
        self.btn1.color = (120, 120, 120)
        self.btn2 = QtWidgets.QPushButton()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

    def color_btn_click(self, widget):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.set_color(widget, color)

    def set_color(self, widget, color):
        widget.setStyleSheet("background-color:rgb({0},{1},{2})".format(*color.getRgb()))
        widget.color = color
    
    def eventFilter(self, obj, event):
        if obj in {self.color1_btn, self.color2_btn}:
            if event.type() == QtCore.QEvent.MouseMove and obj.color:
                mimedata = QtCore.QMimeData()
                mimedata.setColorData(obj.color)
                print obj.color
                print type(obj.color)
                
                pixmap = QtGui.QPixmap(20, 20)
                pixmap.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(pixmap)
                painter.setRenderHint(QtGui.QPainter.Antialiasing)
                painter.setBrush(obj.color)
                painter.setPen(QtGui.QPen(obj.color.darker(150), 2))
                painter.drawEllipse(pixmap.rect().center(), 8, 8)
                painter.end()
                
                drag = QtGui.QDrag(obj)
                drag.setMimeData(mimedata)
                drag.setPixmap(pixmap)
                drag.setHotSpot(pixmap.rect().center())
                drag.exec_(QtCore.Qt.CopyAction)
                
            elif event.type() == QtCore.QEvent.DragEnter:
                event.accept() if event.mimeData().hasColor() else event.ignore()

            elif event.type() == QtCore.QEvent.Drop:
                self.set_color(obj, event.mimeData().colorData())
                event.accept()
                
        return super(DragTest, self).eventFilter(obj, event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = DragTest()
    win.show()
    sys.exit(app.exec_())