# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\App_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(465, 267)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(370, 90, 77, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Button_WebCam_Start = QtWidgets.QPushButton(self.layoutWidget)
        self.Button_WebCam_Start.setObjectName("Button_WebCam_Start")
        self.gridLayout_3.addWidget(self.Button_WebCam_Start, 0, 0, 1, 1)
        self.Button_WebCam_Stop = QtWidgets.QPushButton(self.layoutWidget)
        self.Button_WebCam_Stop.setObjectName("Button_WebCam_Stop")
        self.gridLayout_3.addWidget(self.Button_WebCam_Stop, 1, 0, 1, 1)
        self.app_text_view = QtWidgets.QTextEdit(self.centralwidget)
        self.app_text_view.setGeometry(QtCore.QRect(20, 10, 341, 151))
        self.app_text_view.setObjectName("app_text_view")
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 170, 341, 51))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Button_Setting = QtWidgets.QPushButton(self.layoutWidget_2)
        self.Button_Setting.setObjectName("Button_Setting")
        self.gridLayout_2.addWidget(self.Button_Setting, 0, 0, 1, 1)
        self.Button_Mouse = QtWidgets.QPushButton(self.layoutWidget_2)
        self.Button_Mouse.setObjectName("Button_Mouse")
        self.gridLayout_2.addWidget(self.Button_Mouse, 0, 1, 1, 1)
        self.Button_Keyboard = QtWidgets.QPushButton(self.layoutWidget_2)
        self.Button_Keyboard.setObjectName("Button_Keyboard")
        self.gridLayout_2.addWidget(self.Button_Keyboard, 0, 2, 1, 1)
        self.Button_Exit = QtWidgets.QPushButton(self.layoutWidget_2)
        self.Button_Exit.setObjectName("Button_Exit")
        self.gridLayout_2.addWidget(self.Button_Exit, 0, 3, 1, 1)
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(370, 10, 77, 81))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Button_Dev_Mode = QtWidgets.QPushButton(self.layoutWidget_3)
        self.Button_Dev_Mode.setObjectName("Button_Dev_Mode")
        self.gridLayout.addWidget(self.Button_Dev_Mode, 0, 0, 1, 1)
        self.Button_Release_Mode = QtWidgets.QPushButton(self.layoutWidget_3)
        self.Button_Release_Mode.setObjectName("Button_Release_Mode")
        self.gridLayout.addWidget(self.Button_Release_Mode, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 465, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Button_WebCam_Start.setText(_translate("MainWindow", "웹캠 테스트"))
        self.Button_WebCam_Stop.setText(_translate("MainWindow", "웹캠 중단"))
        self.Button_Setting.setText(_translate("MainWindow", "SETTING"))
        self.Button_Mouse.setText(_translate("MainWindow", "MOUSE"))
        self.Button_Keyboard.setText(_translate("MainWindow", "KEYBOARD"))
        self.Button_Exit.setText(_translate("MainWindow", "EXIT"))
        self.Button_Dev_Mode.setText(_translate("MainWindow", "개발 모드"))
        self.Button_Release_Mode.setText(_translate("MainWindow", "릴리즈 모드"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())