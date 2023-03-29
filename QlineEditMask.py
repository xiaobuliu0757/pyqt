import sys
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QWidget, QApplication


class QlineEditMask(QWidget):
    def __init__(self):
        super(QlineEditMask,self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('用掩码限制QLineEdit控件的输入')
        formLayout = QFormLayout()

        iplineEdit = QLineEdit()
        macLineEdit = QLineEdit()
        dateLineEdit = QLineEdit()
        licenseEdit = QLineEdit()

        iplineEdit.setInputMask('000.000.000.000;_')
        macLineEdit.setInputMask('HH:HH:HH:HH:HH:HH;_')
        dateLineEdit.setInputMask('0000-00-00')
        licenseEdit.setInputMask('>AAAA-AAAA-AAAA-AAAA-AAAA;#')

        formLayout.addRow('数字掩码',iplineEdit)
        formLayout.addRow('mac掩码',macLineEdit)
        formLayout.addRow('日期掩码',dateLineEdit)
        formLayout.addRow('许可证编码',licenseEdit)

        self.setLayout(formLayout)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QlineEditMask()
    main.show()  # 打开窗口
    sys.exit(app.exec_())  # 结束主循环

