# -*- coding:utf-8 -*-

from Qt import QtWidgets, QtCore, QtGui, QtCompat
from functools import partial

import random
import re


class AsiTableView(QtWidgets.QTableView):

    def __init__(self, parent=None):
        super(AsiTableView, self).__init__(parent=parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(40)
        self.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)


class AsiListView(QtWidgets.QListView):

    def __init__(self, parent=None):
        super(AsiListView, self).__init__(parent=parent)

    def mouseReleaseEvent(self, event):
        super(AsiListView, self).mouseReleaseEvent(event)
        event.ignore()

    def mousePressEvent(self, event):
        super(AsiListView, self).mousePressEvent(event)
        event.ignore()


class AsiModel(QtCore.QAbstractTableModel):
    
    __scripts = None
    __colors = None

    @property
    def scripts(self):
        return self.__scripts
    
    @scripts.setter
    def scripts(self, s):
        self.__scripts = s
    
    @property
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c

    def __init__(self, scripts=None, colors=None, parent=None):
        super(AsiModel, self).__init__(parent)
        if scripts is None: 
            self.scripts = [["icon", "label", "author", list(), "annotation", dict()]] # [[icon, label, author, annotation, tags, meta], ...]
        else: 
            self.scripts = scripts 
        if colors is None:
            self.colors = dict()
        else:
            self.colors = colors # {"{tags}":int(0-360), ...}

    def reset(self):
        self.beginResetModel()
        self.scripts = list() 
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.endResetModel()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.scripts)
    
    def columnCount(self, index=QtCore.QModelIndex()):
        return 6
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.scripts[index.row()][index.column()]
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        if role == QtCore.Qt.UserRole:
            return self.colors
        if role == QtCore.Qt.ToolTipRole:
            return self.scripts[index.row()][4]

    def setData(self, index, value, role=None):
        if role == QtCore.Qt.UserRole:
            self.colors = value
            self.dataChanged.emit(index, index)
            return True

        if role != QtCore.Qt.EditRole:
            return False
        
        if index.isValid() and 0 <= index.row() < len(self.scripts):
            self.scripts[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True

        return False
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Icon"
            elif section == 1:
                return "Label"
            elif section == 2:
                return "Author"
            elif section == 3:
                return "Tags"
            elif section == 4:
                return "None"
        if orientation == QtCore.Qt.Vertical:
            return section
        return None

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex(), data=None):
        self.beginInsertRows(QtCore.QModelIndex(), position, position+rows-1)

        for row in range(rows):
            self.scripts.insert(position+row, data)
        self.dataChanged.emit(index, index)

        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)

        del self.scripts[position:position+rows]

        self.endRemoveRows()
        return True


class AsiProxyModel(QtCore.QSortFilterProxyModel):    
    def __init__(self, *args, **kwargs):
        QtCore.QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.line_filter = list()
        self.tag_filter = list()

    def setLineFilter(self, regex):
        if isinstance(regex, unicode):
            if regex:
                regex = regex.lower()
                regex = re.compile(regex)
                temp = list()
                temp.append(regex)
                self.line_filter = temp
            else:
                self.line_filter = list()
        self.invalidateFilter()

    def setTagsFilter(self, tag):
        if isinstance(tag, unicode):
            tag = tag.lower()
            regex = re.compile(tag)
        self.tag_filter.append(regex)
        self.invalidateFilter()

    def clearTagsFilter(self, tag):
        if isinstance(tag, unicode):
            tag = tag.lower()
            regex = re.compile(tag)
        if regex in self.tag_filter:
            self.tag_filter.remove(regex)
        self.invalidateFilter()

    def clearTagsFilters(self):
        self.tag_filter = list()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if (not self.line_filter) and (not self.tag_filter):
            return True
        label, author, tags, annotation = (1, 2, 3, 4)

        def filtering(reg, data, results):
            if isinstance(data, list):
                for d in data:
                    filtering(reg, d, results)
            else:
                data = data.lower()
                results.append(reg.search(data))
        
        tags_results = list()
        line_results = list()

        data = list()
        for column in [label, author, tags, annotation]:
            index = self.sourceModel().index(source_row, column, source_parent)
            if index.isValid():
                data.append(self.sourceModel().data(index, QtCore.Qt.DisplayRole))
        
        for reg in self.tag_filter:
            filtering(reg, data, tags_results)
        
        for reg in self.line_filter:
            filtering(reg, data, line_results)
        
        if self.tag_filter:
            tag_bool = any(tags_results)
        else: 
            tag_bool = True
        if self.line_filter:
            line_bool = any(line_results)
        else:
            line_bool = True

        return all([tag_bool, line_bool])


class AsiTableDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(AsiTableDelegate, self).__init__(parent)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        if index.column() == 0:
            # proxy_model = index.model()
            # source_index = proxy_model.mapToSource(index)

            icon = QtGui.QIcon(index.data())
            icon.paint(painter, option.rect, QtCore.Qt.AlignCenter)
        elif index.column() == 3: 
            # proxy_model = index.model()
            # source_index = proxy_model.mapToSource(index)
            editor = AsiTags()

            if option.state & QtWidgets.QStyle.State_Selected:
                editor.setBackgroundRole(QtGui.QPalette.ColorRole.Highlight)
            
            painter.save()
            editor.colors = index.model().sourceModel().colors
            editor.setup_ui(index.data())
            editor.vis_button(switch=False)

            painter.translate(option.rect.topLeft())
            editor.resize(option.rect.size())
            editor.render(painter, QtCore.QPoint(0, 0))
            painter.restore()
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    # def sizeHint(self, option, index):
    #     if index.column() == 1:
    #         return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
    #     elif index.column() == 3:
    #         editor = AsiTags()
    #         editor.colors = index.model().sourceModel().colors
    #         editor.setup_ui(index.data())
    #         return editor.sizeHint()
    #     else:
    #         return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)

    def createEditor(self, parent, option, index):
        if index.column() == 3:
            # proxy_model = index.model()
            # source_index = proxy_model.mapToSource(index)
            editor = AsiTags(parent=parent)
            editor.colors = index.model().sourceModel().colors
            editor.setup_ui(index.data())
            editor.vis_button(switch=True)
            return editor
            # return AsiTags(parent=parent)
        else:
            return QtWidgets.QStyledItemDelegate.createEditor(self, parent, option, index)

    # def setEditorData(self, editor, index):
    #     if index.column() == 3:
    #         editor.colors = index.model().colors
    #         editor.clear_tags()
    #         editor.setup_ui(index.data())
    #         editor.vis_button(switch=True)
    #     else:
    #         QtWidgets.QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == 3:
            index = model.mapToSource(index)
            model = model.sourceModel()
            model.setData(index, editor.tags, QtCore.Qt.EditRole)
            tags_set = set()
            for row in range(model.rowCount()):
                tags = model.data(index=model.index(row, 3), role=QtCore.Qt.DisplayRole)
                for tag in tags:
                    tags_set.add(tag)
            colors = model.colors
            tags_color = colors.keys()
            for tag in tags_color:
                if tag not in tags_set:
                    del colors[tag] 
            model.setData(index, colors, QtCore.Qt.UserRole)
        else:
            QtWidgets.QStyledItemDelegate.setModelData(self, editor, model, index)


class AsiTags(QtWidgets.QWidget):

    __colors = None

    @property
    def colors(self):
        return self.__colors
    
    @colors.setter
    def colors(self, c):
        self.__colors = c

    def __init__(self, parent=None):
        super(AsiTags, self).__init__(parent)
        
        self.tags = list()
        self.x_buttons = list()
        self.create_ui()

    def create_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self) # TODO : custom layout
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.tag_layout = QtWidgets.QHBoxLayout()
        self.tag_layout.setContentsMargins(7, 7, 7, 7)
        self.tag_layout.setSpacing(6)

        self.line_layout = QtWidgets.QHBoxLayout()
        self.line_layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addLayout(self.tag_layout)
        self.layout.addLayout(self.line_layout)
        self.layout.addStretch(True)

        self.line = QtWidgets.QLineEdit()
        self.line.returnPressed.connect(self.entered_line)
        self.line_layout.addWidget(self.line)
        self.line.hide()

        self.spacer = QtWidgets.QSpacerItem(4, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Base)

    def create_tag(self, name, color):
        count = self.tag_layout.count()
        if count > 0:
            spacer = self.tag_layout.takeAt(count-1)
            del spacer
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("QFrame {{\nbackground-color: hsva({0}, 100, 222, 255);\nborder-radius: 4px;\n}}".format(color))
        frame.setFixedHeight(24)
        label = QtWidgets.QLabel(name)
        label.setStyleSheet("QLabel {\ncolor: #000000;}")
        label.setAlignment(QtCore.Qt.AlignCenter)
        button = QtWidgets.QPushButton("X")
        button.setFixedSize(16, 16)
        
        frame_layout = QtWidgets.QHBoxLayout(frame)
        frame_layout.addWidget(label)
        frame_layout.addWidget(button)
        frame_layout.setContentsMargins(4, 4, 4, 4)
        frame_layout.setSpacing(4)

        self.tag_layout.addWidget(frame)
        self.tag_layout.insertSpacerItem(-1, self.spacer)
        button.clicked.connect(partial(self.delete_tag, tag=frame, name=name))
        self.x_buttons.append(button)
        self.tags.append(name)
        self.tags.sort()

    def vis_button(self, switch):
        if switch is True: 
            self.line.show()
            for button in self.x_buttons: button.show()
        elif switch is False: 
            self.line.hide()
            for button in self.x_buttons: button.hide()
        self.setMinimumSize(self.layout.sizeHint())

    def delete_tag(self, tag, name):
        tag.hide()
        self.tags.remove(name)

    def setup_ui(self, data):
        for tag in data: self.create_tag(name=tag, color=self.colors[tag])
    
    def entered_line(self):
        txt = self.line.text()
        if not txt:
            return
        check_list = set()
        for s in txt:
            if " " == s:
                check_list.add(True)
            else:
                check_list.add(False)
        if len(check_list) > 1:
            return
        if txt in self.tags:
            return

        if self.colors.has_key(txt):
            color = self.colors[txt]
        else:
            color = random.randint(0, 360)
            self.colors[txt] = color
        self.create_tag(name=txt, color=color)
        self.line.clear()

