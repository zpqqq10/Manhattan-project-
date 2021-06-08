from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import pandas as pd
# from .resource_rc import *

class QtTable(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super(QAbstractTableModel, self).__init__(parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]
    
    def columnCount(self, parent=None):
        return self._data.shape[1]
    
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        self._data.iloc[index.row(),index.column()] = value
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

class Sheet(QWidget):
    def __init__(self, header, dataframe=None, parent=None):
        super(Sheet, self).__init__(parent)
        if dataframe is None:
            dataframe = pd.DataFrame(columns=header)
        self.tablemodel = QtTable(dataframe, self)
        self.tableview = QTableView()
        self.tableview.setModel(self.tablemodel)
        self.push_btn = QPushButton("增加行")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tableview)
        self.layout.addWidget(self.push_btn)
        self.setLayout(self.layout)
        self.push_btn.clicked.connect(self._clicked_callback)
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
    
    def _clicked_callback(self, index):
        columns = self.tablemodel._data.columns
        s2 = pd.Series(['' for i in range(len(columns))], index=columns)
        self.tablemodel._data = self.tablemodel._data.append(s2, ignore_index=True)
        self.tablemodel.layoutChanged.emit()
    
    def setData(self, data):
        self.tablemodel._data = data
        self.tablemodel.layoutChanged.emit()

    def getData(self):
        return self.tablemodel._data

class SheetManager(QTabWidget):
    def __init__(self, parent=None):
        super(SheetManager, self).__init__(parent)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        # debug
        self.tab_rowdata = \
        Sheet([
            "时间","顶压(kPa)","透气性指数(t/h)","富氧流量(vol%)",
            "顶温(℃)","全压差(kPa)","热风压(kPa)","实际风速(m/s)",
            "鼓风湿度(vol%)","本小时实际喷煤量"])
        self.tab_label = \
        Sheet(["时间", "硅含量"])
        self.addTab(self.tab_rowdata, "传感器数据(ROWDATA)")
        self.addTab(self.tab_label, "采样数据(LABEL)")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv) # std : create QApplication
    app.aboutToQuit.connect(app.deleteLater)
    main = SheetManager()
    main.show()
    sys.exit(app.exec_()) # std : exits python when the app finishes