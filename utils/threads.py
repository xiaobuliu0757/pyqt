from PyQt5.QtCore import QThread,pyqtSignal
import requests

class NewTaskThread(QThread):
    #信号，触发信号，更新窗体中的数据
    success = pyqtSignal(int,str,str,str)
    error = pyqtSignal(int,str,str,str)
    def __init__(self,row_index,asin,*args,**kwagrs):
        super().__init__(*args,**kwagrs)
        self.row_index = row_index
        self.asin = asin
    def run(self):
        #具体线程应该做的事
        try:
            result = requests.request("GET", url="https://tianqi.2345.com/Pc/apiGet15Days")
            data = result.json()
            # print(type(data))
            date = data["data"][0]["date"]
            week = data["data"][0]["week"]
            weather = data["data"][0]["weather"]

            self.success.emit(self.row_index, date,week,weather)
        except Exception as e:
            self.error.emit(self.row_index,"xx","xx",str(e))



if __name__ == '__main__':
    a = NewTaskThread(1,1).run()
