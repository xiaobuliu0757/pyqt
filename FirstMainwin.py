import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon


class FirstMainWin(QMainWindow):
    def __init__(self):
        super(FirstMainWin, self).__init__()  # 调用父类
        # 设置主窗口的标题
        self.setWindowTitle("第一个主窗口的应用")
        # 设置窗口的尺寸
        self.resize(400, 300)
        self.status = self.statusBar()
        self.status.showMessage("只存在5s的消息", 5000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./OIP-C.jpeg'))
    main = FirstMainWin()
    main.show()  #打开窗口
    sys.exit(app.exec_()) #结束主循环
