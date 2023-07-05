# main.py : 프로그램 시작점.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from App import App_Control

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("가상 인터페이스 프로그램")
        # loadUi("Main_testui.ui", self)  # 추후 UI 파일 제작 후 적용하기.
        self.setGeometry(100, 100, 300, 200)

        # 확인 버튼
        confirm_button = QPushButton("실행", self)
        confirm_button.clicked.connect(self.open_app_window)
        confirm_button.setGeometry(50, 50, 100, 50)

        # 취소 버튼
        cancel_button = QPushButton("종료", self)
        cancel_button.clicked.connect(self.close)
        cancel_button.setGeometry(150, 50, 100, 50)

    def open_app_window(self):
        self.app_window = App_Control()
        self.app_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



__copyright__    = 'Copyright (C) 2023 '
__version__      = ''
__license__      = ''
__author__       = ''
__author_email__ = ''
__url__          = ''

