from PySide2 import QtWidgets, QtCore, QtGui
from common.gui.workspacecontrol import CustomUI

import os


class RoomUI(QtWidgets.QDialog, CustomUI):

    WINDOW_TITLE = 'Room'
    UI = os.path.normpath(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'))

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        
        # ui create
        CustomUI.__init__(self) #
        
    def showEvent(self, e):
        super(RoomUI, self).showEvent(e)

        print 'showEvent'
    
    def closeEvent(self, e):
        super(RoomUI, self).closeEvent(e)

        print 'closeEvent'
    
    def hideEvent(self, e):
        super(RoomUI, self).hideEvent(e)

        print 'hideEvent'
