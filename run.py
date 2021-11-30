import csv
import sys
from builtins import print, len
from datetime import datetime
from glob import glob
from pathlib import Path
from time import sleep

import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QColor, QIcon
from PyQt5.QtWidgets import *
import paramiko
from scp import SCPClient, SCPException


class SSHManager:
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """Create SSH client session to remote server"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """Send a single file to remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()


ssh_manager2 = SSHManager()  ##수신
ssh_manager2.create_ssh_client("192.168.1.6", "user", "user")

form_class = uic.loadUiType("traffic_ui.ui")[0]
stop_check = False

import os


def get_hex():
    ssh_manager2.get_file('/home/user/signal/signal', './signal_recieve')
    with open("signal_recieve", "r") as f2:
        item = f2.readline()
        # print("\r\r\r\r ------,", item)
    f2.close()
    print(item)
    print(item[13])
    return item


def hex_to_step():
    step = get_hex()[14:15]
    return step


def get_int_step():
    print(int(get_hex()[13]))
    return int(get_hex()[13])


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
            self.setIcon(QIcon("image/folder.ico"))
        else:
            self.setText(txt + ".csv")
            self.setIcon(QIcon("image/file.ico"))


class Thread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.data = []
        self.sum = []
        f = open("traffic.csv", "r", encoding="utf-8")
        rdr = csv.reader(f)
        for idx, line in enumerate(rdr):
            self.data.extend([line])  # 인풋 방식 모름
            self.sum.append(self.data[idx][:-1])
        f.close()
        self.inform_dict = {"RED": 0, "YELLOW": 0, "LEFT": 0, "GREEN": 0}
        self.PREVIOUS = self.inform_dict.copy()
        self.CURRENT_TIME = get_int_step()
        self.checkSignal()

    def checkSignal(self):
        df2 = pd.read_csv("traffic.csv")
        inform_by_step = df2[df2['STEP'] == int(get_int_step())]
        self.PREVIOUS = self.inform_dict.copy()
        # print(int(get_int_step()), self.inform_dict, inform_by_step)
        for k in self.inform_dict.keys():
            if k in inform_by_step:
                self.inform_dict[k] = int(inform_by_step[k])

    def run(self):
        global stop_check
        while True:
            if stop_check:
                print(self.CURRENT_TIME, get_int_step())
                if self.CURRENT_TIME != get_int_step():
                    self.checkSignal()
                    if self.PREVIOUS is not self.inform_dict:
                        print(self.PREVIOUS)

                    self.signal.emit(self.PREVIOUS)
                    self.CURRENT_TIME = get_int_step()
                sleep(0.1)


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
        self.event_log.setWindowTitle("신호등")
        self.event_log.setFont(QFont("나눔스퀘어_ac", 12))
        self.set_tree_view()

    def log(self, record):
        self.event_log.append(datetime.today().strftime("[%Y-%m-%d %H-%M-%S] \n" + record))

    def stop(self):
        global stop_check
        if stop_check:
            stop_check = False
            self.start_button.setText("실행")
            self.start_button.repaint()
            self.log("정지")
        else:
            stop_check = True
            self.start_button.setText("정지")
            self.start_button.repaint()
            self.log("실행")

    def start_function(self):
        self.stop()

    def save_function(self):
        global stop_check

        buttonReply = QMessageBox.information(
            self, '저장', "정말로 저장 하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            stop_check = False
            self.start_button.setText("실행")
            self.start_button.repaint()
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
                data.extend([[self.tableWidget.item(row, 0).text(), self.tableWidget.item(row, 1).text(), self.tableWidget.item(row, 2).text()]])
            print(data)
            if len(data) != 0:
                file = open(path, "w", newline="")
                wr = csv.writer(file)
                wr.writerow(["신호", "시간", "스텝"])
                for row in data:
                    wr.writerow(row)
                file.close()

            self.set_tree_view()
            self.log("정지\n데이터가 저장되었습니다\n테이블을 초기화합니다")
            self.tableWidget.setRowCount(0)
        else:
            pass

    def delete_function(self):
        if len(self.treeView.selectedIndexes()) == 1:
            root = self.check_sel_root()
            if os.path.isfile(root):
                os.remove(root)
                self.set_tree_view()
                self.log(root + "\n파일을 삭제했습니다")

    def check_sel_root(self):
        if len(self.treeView.selectedIndexes()) != 0:
            index = self.treeView.selectedIndexes()[0]
            print(index.data())
            root = "C:/traffic_data/"
            file = index.model().itemFromIndex(index).text()
            folder = file.split()[0] + "/"
            return root + folder + file

    def set_tree_view(self):
        self.treeView.setHeaderHidden(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)

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
        self.treeView.doubleClicked.connect(self.check_window)

    def check_window(self):
        if len(self.treeView.selectedIndexes()) != 0:
            root = self.check_sel_root()
            if os.path.isfile(root):
                print("뷰어 클릭")
                os.popen(root)
                self.log(root + "\n파일을 열었습니다")

    def resizeEvent(self, event):
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        # self.start_button.resize(self.mainWindow.sizeHint())
        print("전체", self.centralwidget.width())
        print("테이블", self.tableWidget.width())

    def closeEvent(self, event):
        self.save_function()

    @pyqtSlot(dict)
    def change_traffic_light(self, signals):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        activeData = ""
        for key, value in signals.items():
            if value == 1:
                activeData += key + " "
        self.log(str(activeData + "데이터를 받았습니다\n" + str(get_int_step()) + "스텝"))
        self.event_log.verticalScrollBar().setValue(self.event_log.verticalScrollBar().maximum())
        lists = [QTableWidgetItem(activeData), QTableWidgetItem(datetime.today().strftime("%Y/%m/%d %H:%M:%S")), QTableWidgetItem(str(get_int_step())+" 스텝")]
        for index, row in enumerate(lists):
            self.tableWidget.setItem(rowPosition, index, row)
            self.tableWidget.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
            self.tableWidget.item(rowPosition, index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.tableWidget.scrollToBottom()

        self_signal__lst = [self.RED, self.YELLOW, self.LEFT, self.GREEN]
        for self_signal in self_signal__lst:
            self_signal.setStyleSheet("color: rgb(0, 0, 0);\n"
                                      "background-color: rgb(0, 0, 0);\n"
                                      "line-height: 100px;\n"
                                      "border-radius: 50px;\n"
                                      "min-height: 100px;\n"
                                      "min-width: 100px;")

        for key, value in signals.items():
            print(type(key), type(value))
            if value == 1:
                if key.__eq__("RED"):
                    self.RED.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                           "border-radius: 50px;\n"
                                           "min-height: 100px;\n"
                                           "min-width: 100px;")
                if key.__eq__("YELLOW"):
                    self.YELLOW.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                              "border-radius: 50px;\n"
                                              "min-height: 100px;\n"
                                              "min-width: 100px;")

                if key.__eq__("LEFT"):
                    self.LEFT.setStyleSheet("color: rgb(0, 255, 0);\n"
                                            "background-color: rgb(0, 0, 0);\n"
                                            "line-height: 50px;\n"
                                            "border-radius: 50px;\n"
                                            "border: 5px solid rgb(0, 255, 0);\n"
                                            "min-height: 100px;\n"
                                            "min-width: 100px;")
                if key.__eq__("GREEN"):
                    self.GREEN.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                             "border-radius: 50px;\n"
                                             "min-height: 100px;\n"
                                             "min-width: 100px;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
