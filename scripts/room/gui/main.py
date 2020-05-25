from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
# from common.gui.uiloader import UiLoader

import os


class UiLoader(QtUiTools.QUiLoader):

    _baseinstance = None

    def createWidget(self, classname, parent=None, name=''):
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super(UiLoader, self).createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)

        return widget
    
    def loadUi(self, uifile, baseinstance=None):
        self._baseinstance = baseinstance
        widget = self.load(uifile)
        # QtCore.QMetaObject.connectSlotByName(widget)

        return widget


class RoomUI(QtWidgets.QDialog):

    WINDOW_TITLE = 'Room'
    UI = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'))
    PREFERENCEUI = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'preferenceButton.ui'))

    def __init__(self):
        super(RoomUI, self).__init__()
        UiLoader().loadUi(uifile=self.UI, baseinstance=self)
        
        self.level = 0
        self.create_preference()

    def create_preference(self):
        for i in range(30):
            preferenceButton = QtWidgets.QWidget()
            UiLoader().loadUi(uifile=self.PREFERENCEUI, baseinstance=preferenceButton)
            preferenceButton.resize(128, 128)
            
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(128, 128))

            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, preferenceButton)

    def showEvent(self, e):
        super(RoomUI, self).showEvent(e)

        print('showEvent')
    
    def closeEvent(self, e):
        super(RoomUI, self).closeEvent(e)

        print('closeEvent')
    
    def hideEvent(self, e):
        super(RoomUI, self).hideEvent(e)

        print('hideEvent')























if __name__ == "__main__":
    """ Run the application. """
    from PySide2.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                                   QAbstractItemView)
    import sys

    sys.path.append('D:\\maya')
    app = QApplication(sys.argv)

    test3ui = RoomUI()
    test3ui.show()
    # a = QtWidgets.QFrame()
    # UiLoader().loadUi(uifile=os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'preferenceButton.ui')), baseinstance=a)
    # a.show()

    sys.exit(app.exec_())
