import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from datetime import datetime
from time import sleep

form_class = uic.loadUiType("traffic_ui.ui")[0]


class Thread1(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        signals = ['GREEN', 'YELLOW', 'LEFT', 'YELLOW', 'RED']
        while True:
            for signal in signals:

                self.signal.emit(signal)
                if signal == 'RED':
                    self.parent.RED.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                  "border-radius: 50px;\n"
                                                  "min-height: 100px;\n"
                                                  "min-width: 100px;")
                    sleep(1)
                    self.parent.RED.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                  "border-radius: 50px;\n"
                                                  "min-height: 100px;\n"
                                                  "min-width: 100px;")
                elif signal == 'YELLOW':
                    self.parent.YELLOW.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                                     "border-radius: 50px;\n"
                                                     "min-height: 100px;\n"
                                                     "min-width: 100px;")
                    sleep(1)
                    self.parent.YELLOW.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                     "border-radius: 50px;\n"
                                                     "min-height: 100px;\n"
                                                     "min-width: 100px;")
                elif signal == 'GREEN':
                    self.parent.GREEN.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                    "border-radius: 50px;\n"
                                                    "min-height: 100px;\n"
                                                    "min-width: 100px;")
                    sleep(1)
                    self.parent.GREEN.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                                    "border-radius: 50px;\n"
                                                    "min-height: 100px;\n"
                                                    "min-width: 100px;")
                elif signal == 'LEFT':
                    self.parent.LEFT.setStyleSheet("color: rgb(0, 255, 0);\n"
                                                   "background-color: rgb(0, 0, 0);\n"
                                                   "line-height: 100px;\n"
                                                   "border-radius: 50px;\n"
                                                   "border: 3px solid rgb(0, 255, 0);\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")
                    sleep(1)
                    self.parent.LEFT.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                   "background-color: rgb(0, 0, 0);\n"
                                                   "line-height: 100px;\n"
                                                   "border-radius: 50px;\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("신호등")
        self.setFont(QFont('나눔스퀘어_ac', 12))
        # self.setFixedSize(self.size())
        h1 = Thread1(self)
        h1.signal.connect(self.change_traffic_light)
        h1.start()
        self.pushButton.clicked.connect(self.button1Function)
        self.pushButton_2.clicked.connect(self.button2Function)

    def button1Function(self):
        print("삭제버튼을 눌렀습니다")

    def button2Function(self):
        print("저장버튼을 눌렀습니다")

    @pyqtSlot(str)
    def change_traffic_light(self, signal):
        if signal == 'RED':
            # print(signal + "시그널을 Slot으로 받았습니다")
            pass
        elif signal == 'YELLOW':
            # print(signal + '시그널을 Slot으로 받았습니다')
            pass
        elif signal == 'LEFT':
            # print(signal + '시그널을 Slot으로 받았습니다')
            pass
        elif signal == 'GREEN':
            # print(signal + '시그널을 Slot으로 받았습니다')
            pass
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(datetime.today().strftime("%Y/%m/%d\n%H:%M:%S")))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(signal))
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.scrollToBottom()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
