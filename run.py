import sys

# import self as self
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
from datetime import datetime

form_class = uic.loadUiType("traffic_ui.ui")[0]


class Thread1(QThread):
    signal = pyqtSignal(str, int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        signals = ['RED', 'YELLOW', 'GREEN', 'LEFT']
        cnt = 0
        while True:
            for signal in signals:
                self.signal.emit(signal, cnt)
                cnt = cnt + 1
                if signal == 'RED':
                    self.parent.RED.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                  "border-radius: 45px;\n"
                                                  "min-height: 10px;\n"
                                                  "min-width: 10px;")
                    sleep(1)

                    self.parent.RED.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                  "border-radius: 45px;\n"
                                                  "min-height: 10px;\n"
                                                  "min-width: 10px;")
                if signal == 'YELLOW':
                    self.parent.YELLOW.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                                     "border-radius: 45px;\n"
                                                     "min-height: 10px;\n"
                                                     "min-width: 10px;")
                    sleep(1)
                    self.parent.YELLOW.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                     "border-radius: 45px;\n"
                                                     "min-height: 10px;\n"
                                                     "min-width: 10px;")
                if signal == 'GREEN':
                    self.parent.GREEN.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                    "border-radius: 45px;\n"
                                                    "min-height: 10px;\n"
                                                    "min-width: 10px;")
                    sleep(1)
                    self.parent.GREEN.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                    "border-radius: 45px;\n"
                                                    "min-height: 10px;\n"
                                                    "min-width: 10px;")
                if signal == 'LEFT':
                    self.parent.LEFT.setStyleSheet("color: rgb(0, 255, 0);\n"
                                                   "border-radius: 45px;\n"
                                                   "min-height: 10px;\n"
                                                   "min-width: 10px;")
                    sleep(1)
                    self.parent.LEFT.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                   "border-radius: 45px;\n"
                                                   "min-height: 10px;\n"
                                                   "min-width: 10px;")


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("흙살림")
        self.setFont(QFont('나눔스퀘어_ac', 12))
        h1 = Thread1(self)
        h1.signal.connect(self.change_traffic_light)
        h1.start()

    @pyqtSlot(str, int)
    def change_traffic_light(self, signal, cnt):
        if signal == 'RED':
            print(signal + "시그널을 Slot으로 받았습니다")
        elif signal == 'YELLOW':
            print(signal + '시그널을 Slot으로 받았습니다')
        elif signal == 'LEFT':
            print(signal + '시그널을 Slot으로 받았습니다')
        elif signal == 'GREEN':
            print(signal + '시그널을 Slot으로 받았습니다')
        print("시간 : " + datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
        print("신호등 : " + signal)
        print(cnt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
