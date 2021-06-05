import sys
import view


class App(view.QtWidgets.QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.ui = view.Ui_MainWindow(self)
        self.ui.show()

    def processAction(self, msg):
        self.controller.process(msg)

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())