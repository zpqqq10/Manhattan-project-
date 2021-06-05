from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from .resource_rc import *

class Graph(QWidget):
    def __init__(self, parent=None, figsize=[0.1,0.1,0.8,0.8]):
        super(Graph, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)
        self.ax = self.figure.add_axes(figsize)

    def redraw(self, curve):
        self.ax.clear()
        self.ax.plot(np.array(range(len(curve))), curve)
        self.canvas.draw()

class GraphManager(QTabWidget):
    def __init__(self, parent=None):
        super(GraphManager, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setTabPosition(QtWidgets.QTabWidget.North)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.setDocumentMode(False)
        self.setTabsClosable(False)
        self.setMovable(True)
        self.tab_dict = {}
        self.tab_names = [
            "顶压","透气性指数","富氧流量",
            "顶温","全压差","热风压","实际风速",
            "鼓风湿度","本小时实际喷煤量","硅含量"]
        for tab_name in self.tab_names:
            graph = Graph(self)
            self.addTab(graph, tab_name)
            self.tab_dict[tab_name] = graph

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv) # std : create QApplication
    app.aboutToQuit.connect(app.deleteLater)
    main = GraphManager()
    main.show()
    sys.exit(app.exec_()) # std : exits python when the app finishes