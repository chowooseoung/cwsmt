# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui
from Qt.QtCore import (QPointF, QSize, Qt)

PAINTING_SCALE_FACTOR = 20


class Tag(object):

    def __init__(self, tagName):
        self.tag_name = tagName

        self.tag_button = QtWidgets.QToolButton()

    def sizeHint(self):
        return self.tag_button.sizeHint()

    def paint(self, painter, rect, palette, isEditable=False):

        painter.save() # 저장

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True) # 안티엘리어싱 on
        painter.setPen(QtCore.Qt.NoPen) # 펜 off

        if isEditable:
            painter.setBrush(palette.highlight())
        else:
            painter.setBrush(palette.windowText()) # 브러쉬 설정

        yOffset = (rect.height() - PAINTING_SCALE_FACTOR) / 2
        painter.translate(rect.x(), rect.y() + yOffset)
        painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)

        for i in range(self.maxStarCount):
            if i < self.starCount:
                painter.drawPolygon(self.starPolygon, Qt.WindingFill)
            elif isEditable:
                painter.drawPolygon(self.diamondPolygon, Qt.WindingFill)
            painter.translate(1.0, 0.0)

        painter.restore() # 되돌리기
