import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QColor, QIcon
from PyQt5.QtWidgets import *
from datetime import datetime
from time import sleep
import csv
import os
from glob import glob
from pathlib import Path

form_class = uic.loadUiType("traffic_ui.ui")[0]
form_class2 = uic.loadUiType("traffic_ui_sub.ui")[0]
stop_check = False


class subWindow(QMainWindow, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("신호등")
        self.setFont(QFont("나눔스퀘어_ac", 12))
        self.mySub = subWindow()
        self.mySub.show()


class StandardItem(QStandardItem):
    def __init__(self, txt="", font_size=14, path="", set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont("나눔스퀘어_ac", font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
        if os.path.isdir(path):
            self.setText(txt)
            self.setIcon(QIcon("image/folder.png"))
        else:
            self.setText(txt + ".csv")
            self.setIcon(QIcon("image/file.png"))
            self.setCheckable(True)


class Thread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.data = []
        f = open("traffic.csv", "r", encoding="utf-8")
        rdr = csv.reader(f)
        for line in rdr:
            self.data.extend([line])  # 인풋 방식 모름
        f.close()

    def run(self):
        global stop_check
        while True:
            for (a, b) in self.data:
                if stop_check:
                    self.signal.emit(a)
                sleep(int(b))

    def stop(self):
        global stop_check
        if stop_check:
            stop_check = False
            self.parent.start_button.setText("실행")
            self.parent.start_button.repaint()
        else:
            stop_check = True
            self.parent.start_button.setText("멈춤")
            self.parent.start_button.repaint()
        print("멈춤버튼을 눌렀습니다")


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("신호등")
        self.setFont(QFont("나눔스퀘어_ac", 12))
        self.h1 = Thread(self)
        self.h1.signal.connect(self.change_traffic_light)
        self.h1.start()
        self.start_button.clicked.connect(self.start_function)
        self.save_button.clicked.connect(self.save_function)
        self.delete_button.clicked.connect(self.delete_function)
        self.set_tree_view()
        # self.treeView.setIndentation(0)

    def start_function(self):
        self.h1.stop()

    def save_function(self):
        buttonReply = QMessageBox.information(
            self, '저장', "정말로 저장 하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            global stop_check
            stop_check = False
            data = []
            root = "C:/traffic_data/" + datetime.today().strftime("%Y-%m-%d") + "/"
            file_name = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
            extension = ".csv"
            path = root + file_name + extension

            try:
                if not os.path.exists(root):
                    os.makedirs(root)
            except OSError:
                print("이미 파일이 있습니다" + root)

            self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
            row = self.tableWidget.rowCount()
            for row in range(0, row):
                data.extend([[self.tableWidget.item(row, 0).text(), self.tableWidget.item(row, 1).text()]])
            print(data)
            if len(data) != 0:
                f = open(path, "w", newline="")
                wr = csv.writer(f)
                wr.writerow(["신호", "시간"])
                for row in data:
                    wr.writerow(row)
                f.close()

            self.set_tree_view()
            print("저장버튼을 눌렀습니다")
            self.tableWidget.setRowCount(0)
        else:
            print('No clicked.')

    def delete_function(self):
        root = "C:/traffic_data/"
        index = self.treeView.selectedIndexes()[0]
        if index is None:
            pass
        else:
            file = index.model().itemFromIndex(index).text()
            folder = file.split()[0] + "/"
            root2 = root + folder + file
            if os.path.isfile(root2):
                os.remove(root2)
            self.set_tree_view()
            print("삭제버튼을 눌렀습니다")

    def set_tree_view(self):
        self.treeView.setHeaderHidden(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        paths = glob("C:/traffic_data/*")

        for path in paths:
            folder = StandardItem(Path(path).stem, 16, path)
            files = glob(path + "/*")
            for file in files:
                f = StandardItem(Path(file).stem, 14, file)
                folder.appendRow(f)

            rootNode.appendRow(folder)
        self.treeView.setModel(treeModel)
        self.treeView.collapseAll()
        self.treeView.doubleClicked.connect(self.new_window)

    def new_window(self):
        root = "C:/traffic_data/"
        index = self.treeView.selectedIndexes()[0]
        file = index.model().itemFromIndex(index).text()
        folder = file.split()[0] + "/"
        print(root + folder + file)
        if os.path.isfile(root + folder + file):
            subWindow().show()

    @pyqtSlot(str)
    def change_traffic_light(self, signal_data):
        print(signal_data)

        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        lists = [QTableWidgetItem(signal_data), QTableWidgetItem(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))]
        for index, row in enumerate(lists):
            self.tableWidget.setItem(rowPosition, index, row)
            self.tableWidget.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
            self.tableWidget.item(rowPosition, index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.tableWidget.scrollToBottom()

        signal_labels = {"RED": self.RED, "LEFT": self.LEFT, "YELLOW": self.YELLOW, "GREEN": self.GREEN}
        signal_lst = [self.RED, self.LEFT, self.YELLOW, self.GREEN]
        for signal in signal_lst:
            signal.setStyleSheet("color: rgb(0, 0, 0);\n"
                                 "background-color: rgb(0, 0, 0);\n"
                                 "line-height: 100px;\n"
                                 "border-radius: 50px;\n"
                                 "min-height: 100px;\n"
                                 "min-width: 100px;")
            if signal_data.__eq__("RED"):
                signal_labels[signal_data].setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")
            if signal_data.__eq__("YELLOW"):
                signal_labels[signal_data].setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")

            if signal_data.__eq__("LEFT"):
                signal_labels[signal_data].setStyleSheet("color: rgb(0, 255, 0);\n"
                                                         "background-color: rgb(0, 0, 0);\n"
                                                         "line-height: 100px;\n"
                                                         "border-radius: 50px;\n"
                                                         "border: 5px solid rgb(0, 255, 0);\n"
                                                         "box-sizing: border-box;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")

            if signal_data.__eq__("GREEN"):
                signal_labels[signal_data].setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
