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
from PyQt5.QtGui import QIcon


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


def load_project_structure(root, tree):
    import os
    from PyQt5.QtWidgets import QTreeWidgetItem
    for element in os.listdir(root):
        path_info = root + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        if os.path.isdir(path_info):
            load_project_structure(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('image/folder.png'))
        else:
            parent_itm.setIcon(0, QIcon('image/file.png'))


form_class = uic.loadUiType("traffic_ui.ui")[0]
stop_check = False


class Thread1(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.date = []
        f = open('traffic.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)

        for line in rdr:
            self.date.extend([line[0]])
            # self.date.extend([line[1]])
        f.close()

    def run(self):
        global stop_check
        while True:
            for signal in self.date:
                sleep(1)
                if stop_check:
                    self.signal.emit(signal)

    def stop(self):
        global stop_check
        if stop_check:
            stop_check = False
            self.parent.pushButton.setText("실행")
            self.parent.pushButton.repaint()
        else:
            stop_check = True
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
        # load_project_structure("C:/traffic_data/", self.treeWidget)
        self.set_tree_view()
        self.treeView.setIndentation(0)
        self.treeModel2 = QStandardItemModel()
        self.rootNode2 = self.treeModel2.invisibleRootItem()

    def button1Function(self):
        self.h1.stop()

    def button2Function(self):
        global stop_check
        stop_check = False
        data = []
        # root = 'C:/traffic_data/'
        root2 = 'C:/traffic_data/' + datetime.today().strftime("%Y-%m-%d") + "/"
        file_name = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
        extension = '.csv'
        path = root2 + file_name + extension

        try:
            if not os.path.exists(root2):
                os.makedirs(root2)
        except OSError:
            print('이미 파일이 있습니다' + root2)
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
        # load_project_structure("C:/traffic_data/", self.treeWidget)
        self.set_tree_view()
        print("저장버튼을 눌렀습니다")
        self.tableWidget.setRowCount(0)
        # stop_check = True
        self.pushButton.setText("실행")
        self.pushButton.repaint()


    def set_tree_view(self):
        self.treeView.setHeaderHidden(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        paths = glob('C:/traffic_data/*')

        for path in paths:
            folder = StandardItem(Path(path).stem, 16, set_bold=True)
            files = glob(path + '/*')
            for file in files:
                imgs = StandardItem(Path(file).stem, 14)
                folder.appendRow(imgs)

            rootNode.appendRow(folder)

        self.treeView.setModel(treeModel)
        self.treeView.collapseAll()
        # self.treeView.doubleClicked.connect(self.new_window)

    def button3Function(self):

        print("삭제버튼을 눌렀습니다")

    @pyqtSlot(str)
    def change_traffic_light(self, inputsignal):

        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        lists = [QTableWidgetItem(inputsignal), QTableWidgetItem(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))]
        for index, row in enumerate(lists):
            self.tableWidget.setItem(rowPosition, index, row)
            self.tableWidget.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
            self.tableWidget.item(rowPosition, index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.tableWidget.scrollToBottom()

        signal_labels = {'RED': self.RED, 'LEFT': self.LEFT, 'YELLOW': self.YELLOW, 'GREEN': self.GREEN}
        signal_lst = [self.RED, self.LEFT, self.YELLOW, self.GREEN]
        for signal in signal_lst:
            signal.setStyleSheet("color: rgb(0, 0, 0);\n"
                                 "background-color: rgb(0, 0, 0);\n"
                                 "line-height: 100px;\n"
                                 "border-radius: 50px;\n"
                                 "min-height: 100px;\n"
                                 "min-width: 100px;")
            if inputsignal.__eq__('RED'):
                signal_labels[inputsignal].setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")
            if inputsignal.__eq__('YELLOW'):
                signal_labels[inputsignal].setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")

            if inputsignal.__eq__('LEFT'):
                signal_labels[inputsignal].setStyleSheet("color: rgb(0, 255, 0);\n"
                                                         "background-color: rgb(0, 0, 0);\n"
                                                         "line-height: 100px;\n"
                                                         "border-radius: 50px;\n"
                                                         "border: 5px solid rgb(0, 255, 0);\n"
                                                         "box-sizing: border-box;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")

            if inputsignal.__eq__('GREEN'):
                signal_labels[inputsignal].setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                         "border-radius: 50px;\n"
                                                         "min-height: 100px;\n"
                                                         "min-width: 100px;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
