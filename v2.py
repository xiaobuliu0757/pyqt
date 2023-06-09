import json
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QTableWidget, QTableWidgetItem, QLabel, QScrollBar, QMessageBox

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

STATUS_MAPPING = {
    0: '初始化中',
    1: '待执行',
    2: '正在执行',
    3: '完成并提醒',
    10: '异常并停止',
    11: '初始化失败'
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 控件
        self.txt_asin = None
        # 窗体标题和尺寸
        self.setWindowTitle("测试小工具")

        # 窗体的尺寸
        self.resize(800, 450)

        # 窗体的位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 垂直布局
        layout = QVBoxLayout()
        # 引用顶部的函数
        layout.addLayout(self.init_header())
        # 引用中部
        layout.addLayout(self.init_form())
        # 引用表格
        layout.addLayout(self.init_table())
        # 引用底部
        layout.addLayout(self.init_footer())
        # 给窗体设置元素的排列方式/创建布局
        self.setLayout(layout)

    def init_header(self):
        # 1、创建顶部菜单布局
        header_layout = QHBoxLayout()
        # 1.1创建按钮，加入header_layout
        btn_start = QPushButton("开始")
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton("停止")
        header_layout.addWidget(btn_stop)
        # 1.2给顶部菜单布局设置一个弹簧
        header_layout.addStretch()
        return header_layout

    def init_form(self):
        # 2、创建表单布局
        form_layout = QHBoxLayout()
        # 2.1添加输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品id和价格，例如bjjhj=88")  # 输入框默认提示
        self.txt_asin = txt_asin
        form_layout.addWidget(txt_asin)
        # 2.2添加按钮
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)
        form_layout.addWidget(btn_add)

        return form_layout

    # 点击添加按钮
    def event_add_click(self):
        # 1、获取输入框中的内容
        text = self.txt_asin.text()
        # print(text)
        text = text.strip() #去掉空白
        if not text:
            QMessageBox.warning(self,"错误","商品的asin输入错误")
            return
        asin,price = text.split("=")
        # price = float(price)
        # 2、加入到表格中（型号、低价）
        new_row_list = [asin,"","",price,0,0,0,5]

        current_row_count = self.table_widget.rowCount() #当前表格有多少行
        self.table_widget.insertRow(current_row_count)
        for i, ele in enumerate(new_row_list):
            ele = STATUS_MAPPING[int(ele)] if i == 6 else ele
            cell = QTableWidgetItem(str(ele))  # 写个单元格
            if i in [0, 4, 5, 6]:
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 限制单元格内不可修改
            self.table_widget.setItem(current_row_count, i, cell)

        # 3、发送请求自动获取标题(通过爬虫获取数据)
        from utils.threads import NewTaskThread

        thread = NewTaskThread(current_row_count,asin,self)
        thread.success.connect(self.init_task_success_callback)
        thread.error.connect(self.init_task_error_callback)
        thread.start()
        #注意：不能在主线程做爬虫（不然界面会全部卡住），正确操作：创建线程去做爬虫，爬去到数据更新到窗体（信号）
    def init_task_success_callback(self,row_index,asin,title,url):
        #更新窗体显示的数据
        # print(f"成功:{row_index,asin,title,url}")
        #更行表格内容

        cell_title = QTableWidgetItem(title)
        # self.table_widget.setItem(row_index,1,cell_title)  #更新第1列
        self.table_widget.setItem(row_index,1,cell_title)  #更新第1列

        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index,2,cell_url) #更新第2列

        cell_status = QTableWidgetItem(STATUS_MAPPING[3])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.table_widget.setItem(row_index,6,cell_status)  #更新第6列

        self.table_widget.viewport().update()  # 强刷
        self.txt_asin.clear()#清空输入框

    def init_task_error_callback(self,row_index,asin,title,url):
        # 更新窗体显示的数据

        print(row_index,asin,title,url)
        print(f"失败:{row_index, asin, title, url}")

        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)  # 更新第1列

        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)  # 更新第2列

        cell_status = QTableWidgetItem(STATUS_MAPPING[11])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.table_widget.setItem(row_index, 6, cell_status)  # 更新第6列

        self.table_widget.viewport().update()#强刷
        self.txt_asin.clear()  # 清空输入框


    def init_table(self):
        # 3、创建中间表格
        table_layout = QHBoxLayout()

        # 3.1创建表格
        self.table_widget = table_widget = QTableWidget(0, 8)
        table_header = [
            {"filed": "asin", "text": "asin", "width": 120},
            {"filed": "title", "text": "标题", "width": 150},
            {"filed": "url", "text": "url", "width": 400},
            {"filed": "price", "text": "低价", "width": 100},
            {"filed": "success", "text": "成功次数", "width": 100},
            {"filed": "error", "text": "503次", "width": 100},
            {"filed": "status", "text": "状态", "width": 100},
            {"filed": "frequency", "text": "频率（n秒/次）", "width": 100},
        ]
        for idx, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info["text"])
            table_widget.setHorizontalHeaderItem(idx, item)  # 设置表格第一个表头名
            table_widget.setColumnWidth(idx, info["width"])
        # 3.2初始化表格
        # 读取文件
        file_path = os.path.join(BASE_DIR, 'db.json')
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        data_list = json.loads(data)
        current_row_count = table_widget.rowCount()  # 获取当前表格多少行
        for row_list in data_list:
            table_widget.insertRow(current_row_count)
            # print(f"row_list:{row_list}")
            # 写入真实数据
            value = row_list.values()  # 获取所有字典的值
            new_list = list(value)  # 转换一下格式
            for i, ele in enumerate(new_list):
                ele = STATUS_MAPPING[int(ele)] if i == 6 else ele
                cell = QTableWidgetItem(ele)  # 写个单元格
                if i in [0, 4, 5, 6]:
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 限制单元格内不可修改
                table_widget.setItem(current_row_count, i, cell)

        table_layout.addWidget(table_widget)
        return table_layout

    def init_footer(self):
        # 4、创建底部
        footer_layout = QHBoxLayout()
        # 4.1创建按钮
        label_status = QLabel("未检测", self)
        footer_layout.addWidget(label_status)

        footer_layout.addStretch()  # 弹簧

        btn_reinit = QPushButton("重新初始化")
        footer_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton("重新检测")
        footer_layout.addWidget(btn_recheck)

        btn_reset = QPushButton("次数清零")
        footer_layout.addWidget(btn_reset)

        btn_delete = QPushButton("删除检测项目")
        footer_layout.addWidget(btn_delete)

        btn_alert = QPushButton("smtp报警配置")
        footer_layout.addWidget(btn_alert)

        return footer_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()  # 打开主窗口
    sys.exit(app.exec_())  # 结束主循环
