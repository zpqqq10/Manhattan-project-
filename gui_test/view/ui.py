from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .DatabaseManager import *
from .GraphManager import *
from .SheetManager import *
from .Bar import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from .resource_rc import *

class Ui_MainWindow(QMainWindow):
    def __init__(self, top):
        super(Ui_MainWindow, self).__init__()
        self.top = top
        self._load_rc()
        self.resize(1250, 868)
        self.setAcceptDrops(False)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("锅炉硅含量分析")
        self.setWindowIcon(self.boiler_icon)
        self._set_layout()

    def _load_rc(self):
        self.boiler_icon = QtGui.QIcon()
        self.boiler_icon.addPixmap(QtGui.QPixmap(":/boiler.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

    def _set_layout(self):
        """
        central_widget
            vertical_layout_widget
                vertical_layout
                    horizontal_layout
                        graph_tab_widget
                        filem_tree_widget
                    sheet_tab_widget
        """
        # widget layout
        self.toolbar = ToolBar(self)
        self.addToolBar(4, self.toolbar)
        self.central_widget = QtWidgets.QWidget(self)
        self.vertical_layout_widget = QtWidgets.QWidget(self.central_widget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget)
        self.vertical_layout_widget.setGeometry(QtCore.QRect(10, 10, 1231, 790))
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.graph_tab_widget = GraphManager(self)
        self.filem_tree_widget = DatabaseManager(self)
        self.horizontal_layout.addWidget(self.filem_tree_widget)
        self.horizontal_layout.addWidget(self.graph_tab_widget)
        self.sheet_tab_widget = SheetManager(self.vertical_layout_widget)
        self.vertical_layout.addWidget(self.sheet_tab_widget)
        self.vertical_layout.setStretch(0, 1)
        self.vertical_layout.setStretch(1, 1)
        self.horizontal_layout.setStretch(0, 6)
        self.horizontal_layout.setStretch(1, 15)
        self.setCentralWidget(self.central_widget)

    def actionEmitMsg(self, msg):
        print(msg)
        self.top.processAction(msg)
    
    def treeEmitMsg(self, key, value, item):
        print(key, value)
    
    def newDatabase(self, uid):
        return self.filem_tree_widget.newDatabase(uid)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())