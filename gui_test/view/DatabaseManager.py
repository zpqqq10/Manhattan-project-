from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .resource_rc import *

class Database(QTreeWidgetItem):
    def __init__(self, parent, uid):
        super(Database, self).__init__(parent)
        self.uid = uid
        self.parent = parent
        self.setText(0, 'database')
        self.setText(1, '数据集')
        self.setIcon(0, self.parent.database_icon)
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.child_rowdata = None
        self.child_label = None

    def newSheet(self, type):
        try:
            if type == 'rowdata':
                if self.child_rowdata is not None:
                    raise RuntimeError('[ERROR] Duplicate!')
                self.child_rowdata = QtWidgets.QTreeWidgetItem()
                self.child_rowdata.setFlags(self.child_rowdata.flags() | Qt.ItemIsEditable)
                self.child_rowdata.setText(0, 'rowdata')
                self.child_rowdata.setText(1, 'ROWDATA表单')
                self.child_rowdata.setIcon(0, self.parent.datasheet_icon)
                self.addChild(self.child_rowdata)
                return self.child_rowdata
            elif type == 'label':
                if self.child_label is not None:
                    raise RuntimeError('[ERROR] Duplicate!')
                self.child_label = QtWidgets.QTreeWidgetItem()
                self.child_label.setFlags(self.child_label.flags() | Qt.ItemIsEditable)
                self.child_label.setText(0, 'label')
                self.child_label.setText(1, 'LABEL表单')
                self.child_label.setIcon(0, self.parent.datasheet_icon)
                self.addChild(self.child_label)
                return self.child_label
            else:
                raise RuntimeError('[ERROR] Broken command')
        except RuntimeError as e:
            # print(e)
            return None

class DatabaseManager(QTreeWidget):
    def __init__(self, parent=None):
        super(DatabaseManager, self).__init__(parent)
        self.parent = parent
        self.clicked.connect(self._clicked_callback)
        self._load_rc()
        # """ set layout """
        self.setColumnCount(2)
        self.headerItem().setText(0,"文件名")
        self.headerItem().setText(1,"类型")
        # """ set data """
        self.selectedDatabase = None
        # debug
        # self.newDatabase(1)
        # self.newDatabase(2)
        # self.newDatabase(3)

    def newDatabase(self, uid):
        database = Database(self, uid)
        return database
    
    def newSheet(self, type):
        try:
            item = self.selectedDatabase
            if item is None:
                raise RuntimeError('[ERROR] No database is selected now')
            return item.newSheet(type)
        except RuntimeError as e:
            # print(e)
            return None

    def _load_rc(self):
        self.database_icon = QtGui.QIcon()
        self.datasheet_icon   = QtGui.QIcon()
        self.database_icon.addPixmap(QtGui.QPixmap(":/Folder-Filled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.datasheet_icon.addPixmap(QtGui.QPixmap(":/Database-Filled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    def _clicked_callback(self, qmodeLindex):
        item = self.currentItem()
        if type(item).__name__ == 'Database':
            self.selectedDatabase = item
        elif item is None:
            self.selectedDatabase = None
        if self.parent is not None:
            self.parent.treeEmitMsg(item.text(0), item.text(1), item)

        # debug
        # print('Key=%s, value=%s'%(item.text(0), item.text(1)))
        # if self.selectedDatabase is not None:
        #     self.selectedDatabase.newSheet('rowdata')
        #     self.selectedDatabase.newSheet('label')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv) # std : create QApplication
    app.aboutToQuit.connect(app.deleteLater)
    main = FileManager()
    main.show()
    sys.exit(app.exec_()) # std : exits python when the app finishes