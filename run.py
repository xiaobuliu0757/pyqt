import sys
from signalslot import Ui_MainWindow
from PyQt5.QtWidgets import QApplication,QMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui=Ui_MainWindow()
    #向主窗口添加口内控件
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
