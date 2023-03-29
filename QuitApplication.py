import sys
from PyQt5.QtWidgets import QHBoxLayout,QMainWindow,QApplication,QPushButton,QWidget
'''
1. 导入所需的PyQt5模块和类。
2. 定义一个继承自`QMainWindow`的类`QuitAppliaction`。此类表示应用程序的主窗口。
3. 在类的`__init__`方法中，设置窗口大小、标题，并创建一个带有文本“退出”的`QPushButton`部件。
4. 将按钮的`clicked`信号连接到`onClick_Button`方法。当单击按钮时，将调用此方法。
5. 创建一个`QHBoxLayout`，并将按钮添加到其中。然后，创建一个`QWidget`，并将其布局设置为水平布局。最后，将主窗口的中心部件设置为此部件。
6. 定义`onClick_Button`方法，当单击按钮时调用该方法。在此方法中，打印一条消息，获取`QApplication`实例，并退出应用程序。
7. 在`__main__`块中，创建一个`QApplication`对象，创建`QuitAppliaction`类的实例，显示主窗口，并启动应用程序的主事件循环。'''
import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QPushButton, QWidget

class QuitAppliaction(QMainWindow):
    def __init__(self):
        super(QuitAppliaction, self).__init__()
        self.resize(300, 120)
        self.setWindowTitle('退出应用程序')

        # 添加按钮
        self.button1 = QPushButton('退出')

        # 将信号与槽关联
        self.button1.clicked.connect(self.onClick_Button)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)

        self.setCentralWidget(mainFrame)

    # 按钮单击时间的方法（自定义槽）
    def onClick_Button(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QuitAppliaction()
    main.show()  # 打开窗口
    sys.exit(app.exec_())  # 结束主循环
