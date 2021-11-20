from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(936, 829)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(10, 20, 10, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.traffic_light_widget = QtWidgets.QWidget(self.centralwidget)
        self.traffic_light_widget.setMinimumSize(QtCore.QSize(450, 150))
        self.traffic_light_widget.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.traffic_light_widget.setObjectName("traffic_light_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.traffic_light_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.RED = QtWidgets.QLabel(self.traffic_light_widget)
        self.RED.setMinimumSize(QtCore.QSize(100, 100))
        self.RED.setMaximumSize(QtCore.QSize(100, 100))
        self.RED.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                               "color: rgb(0, 0, 0);\n"
                               "border-radius: 50px;\n"
                               "min-height: 100px;\n"
                               "min-width: 100px;")
        self.RED.setText("")
        self.RED.setObjectName("RED")
        self.horizontalLayout.addWidget(self.RED)
        self.YELLOW = QtWidgets.QLabel(self.traffic_light_widget)
        self.YELLOW.setMaximumSize(QtCore.QSize(100, 100))
        self.YELLOW.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                  "border-radius: 50px;\n"
                                  "min-height: 100px;\n"
                                  "min-width: 100px;")
        self.YELLOW.setText("")
        self.YELLOW.setObjectName("YELLOW")
        self.horizontalLayout.addWidget(self.YELLOW)
        self.LEFT = QtWidgets.QLabel(self.traffic_light_widget)
        self.LEFT.setMinimumSize(QtCore.QSize(90, 90))
        self.LEFT.setMaximumSize(QtCore.QSize(100, 100))
        self.LEFT.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                "background-color: rgb(0, 0, 0);\n"
                                "line-height: 100px;\n"
                                "border-radius: 50px;\n"
                                "min-height: 90px;\n"
                                "min-width: 90px;\n"
                                "")
        self.LEFT.setObjectName("LEFT")
        self.horizontalLayout.addWidget(self.LEFT)
        self.GREEN = QtWidgets.QLabel(self.traffic_light_widget)
        self.GREEN.setMinimumSize(QtCore.QSize(100, 100))
        self.GREEN.setMaximumSize(QtCore.QSize(100, 100))
        self.GREEN.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                 "border-radius: 50px;\n"
                                 "min-height: 100px;\n"
                                 "min-width: 100px;")
        self.GREEN.setText("")
        self.GREEN.setObjectName("GREEN")
        self.horizontalLayout.addWidget(self.GREEN)
        self.horizontalLayout_2.addWidget(self.traffic_light_widget)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 3)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setMinimumSize(QtCore.QSize(450, 100))
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 5, 6, 2)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(450, 100))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(45)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.verticalHeader().setMinimumSectionSize(40)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 6, 3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 70))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 5, 1, 1, QtCore.Qt.AlignVCenter)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 70))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 6, 6, 1, 1, QtCore.Qt.AlignVCenter)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LEFT.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-family:\'Arial\'; font-size:48pt; font-weight:600;\">←</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "LED"))
        self.pushButton.setText(_translate("MainWindow", "삭제"))
        self.pushButton_2.setText(_translate("MainWindow", "저장"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
