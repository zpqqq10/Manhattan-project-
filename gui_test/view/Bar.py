from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .resource_rc import *

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self._load_rc()
        self.parent = parent
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setMovable(False)
        self._add_action()
        self._set_connect()
        self.setWindowTitle("工具栏")

    def _load_rc(self):
        self.open_icon     = QtGui.QIcon()
        self.new_icon      = QtGui.QIcon()
        self.delete_icon   = QtGui.QIcon()
        self.save_icon     = QtGui.QIcon()
        self.up_icon       = QtGui.QIcon()
        self.submit_icon   = QtGui.QIcon()
        self.switch_icon   = QtGui.QIcon()
        self.open_icon.addPixmap(QtGui.QPixmap(":/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_icon.addPixmap(QtGui.QPixmap(":/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_icon.addPixmap(QtGui.QPixmap(":/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_icon.addPixmap(QtGui.QPixmap(":/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up_icon.addPixmap(QtGui.QPixmap(":/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.submit_icon.addPixmap(QtGui.QPixmap(":/submit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.switch_icon.addPixmap(QtGui.QPixmap(":/switch.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    def _add_action(self):
        self.new_dataset = QtWidgets.QAction(self.parent)
        self.create_sheet_1 = QtWidgets.QAction(self.parent)
        self.create_sheet_2 = QtWidgets.QAction(self.parent)
        self.dele = QtWidgets.QAction(self.parent)
        self.save = QtWidgets.QAction(self.parent)
        self.upload = QtWidgets.QAction(self.parent)
        self.submit = QtWidgets.QAction(self.parent)
        self.switch = QtWidgets.QAction(self.parent)
        self.new_dataset.setIcon(self.open_icon)
        self.create_sheet_1.setIcon(self.new_icon)
        self.create_sheet_2.setIcon(self.new_icon)
        self.dele.setIcon(self.delete_icon)
        self.save.setIcon(self.save_icon)
        self.upload.setIcon(self.up_icon)
        self.submit.setIcon(self.submit_icon)
        self.switch.setIcon(self.switch_icon)
        self.new_dataset.setText("新建数据集")
        self.create_sheet_1.setText("新建ROWDATA")
        self.create_sheet_2.setText("新建LABEL")
        self.dele.setText("删除选中项")
        self.save.setText("保存选中项")
        self.upload.setText("打开表单")
        self.submit.setText("递交数据集")
        self.switch.setText("切换绘图模式")
        self.addAction(self.new_dataset)
        self.addAction(self.create_sheet_1)
        self.addAction(self.create_sheet_2)
        self.addAction(self.dele)
        self.addAction(self.upload)
        self.addAction(self.save)
        self.addAction(self.submit)
        self.addAction(self.switch)
    
    def _set_connect(self):
        self.new_dataset.triggered.connect(self._new_dataset_callback)
        self.create_sheet_1.triggered.connect(self._create_sheet_callback_1)
        self.create_sheet_2.triggered.connect(self._create_sheet_callback_2)
        self.dele.triggered.connect(self._dele_callback)
        self.save.triggered.connect(self._save_callback)
        self.upload.triggered.connect(self._upload_callback)
        self.submit.triggered.connect(self._submit_callback)
        self.switch.triggered.connect(self._switch_callback)
    
    def _new_dataset_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_new_dataset_callback')
    def _create_sheet_callback_1(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_create_sheet_callback_1')
    def _create_sheet_callback_2(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_create_sheet_callback_2')
    def _dele_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_dele_callback')
    def _save_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_save_callback')
    def _upload_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_upload_callback')
    def _submit_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_submit_callback')
    def _switch_callback(self):
        if self.parent is not None:
            self.parent.actionEmitMsg('_switch_callback')

    

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ToolBar(MainWindow)
    ui.setGeometry(0,0,1270,60)
    MainWindow.show()
    sys.exit(app.exec_())