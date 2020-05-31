import sys
sys.path.append("D:\maya\scripts")

from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
from common.gui.uiloader import UiLoader

import os


class PreferenceUI(QtWidgets.QDialog):

    

    def __init__(self, json):
        super(PreferenceUI, self).__init__()
        self.json = json

    def init_ui(self):
        self.mainLayout = QtWidgets.QHBoxLayout(self)

        for i in self.json['team']:
            setattr(PreferenceUI, i, QtWidgets.QToolButton())
            toolButton = getattr(PreferenceUI, i)
            self.mainLayout.addWidget(toolButton)

            toolButton.setAuto
            toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            toolButton.setArrowType(QtCore.Qt.RightArrow)
            toolButton.setText("toolButton")
            toolButton.setCheckable(True)
            toolButton.setChecked(False)
            toolButton.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        



if __name__ == "__main__":
    """ Run the application. """
    from PySide2.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                                   QAbstractItemView)
    app = QApplication(sys.argv)

    test3ui = PreferenceUI()
    test3ui.show()

    sys.exit(app.exec_())
