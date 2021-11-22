import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import *
from datetime import datetime
from time import sleep
import csv
import os

form_class = uic.loadUiType("traffic_ui.ui")[0]
stop_check = True


class Thread1(QThread):
    global stop_check
    signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.check = stop_check

    def run(self):
        signals = ['GREEN', 'YELLOW', 'LEFT', 'YELLOW', 'RED']
        while True:
            for signal in signals:
                sleep(1)
                if self.check:
                    self.signal.emit(signal)

    def stop(self):
        if self.check:
            self.check = False
            self.parent.pushButton.setText("실행")
            self.parent.pushButton.repaint()
        else:
            self.check = True
            self.parent.pushButton.setText("멈춤")
            self.parent.pushButton.repaint()
        print("멈춤버튼을 눌렀습니다")


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("신호등")
        self.setFont(QFont('나눔스퀘어_ac', 12))
        self.h1 = Thread1(self)
        self.h1.signal.connect(self.change_traffic_light)
        self.h1.start()
        self.pushButton.clicked.connect(self.button1Function)
        self.pushButton_2.clicked.connect(self.button2Function)
        self.pushButton_3.clicked.connect(self.button3Function)

    def button1Function(self):
        self.h1.stop()

    def button2Function(self):
        self.h1.stop()
        data = []
        root = 'C:/traffic_data/'
        root2 = 'C:/traffic_data/' + datetime.today().strftime("%Y-%m-%d") + "/"
        file_name = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
        extension = '.csv'
        path = root2 + file_name + extension

        try:
            if not os.path.exists(root2):
                os.makedirs(root2)
        except OSError:
            print('이미 파일이 있습니다' + root2)

        row = self.tableWidget.rowCount()
        for row in range(0, row):
            data.extend([[self.tableWidget.item(row, 0).text(), self.tableWidget.item(row, 1).text()]])

        f = open(path, "w", newline="")
        wr = csv.writer(f)
        for row in data:
            wr.writerow(row)
        f.close()

        print("저장버튼을 눌렀습니다")
        self.h1.stop()
        self.tableWidget.setRowCount(0)

    def button3Function(self):
        print("삭제버튼을 눌렀습니다")

    @pyqtSlot(str)
    def change_traffic_light(self, input):

        signal_labels = {'RED': self.RED, 'LEFT': self.LEFT, 'YELLOW': self.YELLOW, 'GREEN': self.GREEN}
        signal_lst = [self.RED, self.LEFT, self.YELLOW, self.GREEN]
        for signal in signal_lst:
            signal.setStyleSheet("color: rgb(0, 0, 0);\n"
                                 "background-color: rgb(0, 0, 0);\n"
                                 "line-height: 100px;\n"
                                 "border-radius: 50px;\n"
                                 "min-height: 100px;\n"
                                 "min-width: 100px;")
            if input.__eq__('RED'):
                signal_labels[input].setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                   "border-radius: 50px;\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")
            if input.__eq__('YELLOW'):
                signal_labels[input].setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                                   "border-radius: 50px;\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")

            if input.__eq__('LEFT'):
                signal_labels[input].setStyleSheet("color: rgb(0, 255, 0);\n"
                                                   "background-color: rgb(0, 0, 0);\n"
                                                   "line-height: 100px;\n"
                                                   "border-radius: 50px;\n"
                                                   "border: 3px solid rgb(0, 255, 0);\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")

            if input.__eq__('GREEN'):
                signal_labels[input].setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                   "border-radius: 50px;\n"
                                                   "min-height: 100px;\n"
                                                   "min-width: 100px;")

        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        lists = [QTableWidgetItem(input), QTableWidgetItem(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))]
        for index, row in enumerate(lists):
            self.tableWidget.setItem(rowPosition, index, row)
            self.tableWidget.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
            self.tableWidget.item(rowPosition, index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.tableWidget.scrollToBottom()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
