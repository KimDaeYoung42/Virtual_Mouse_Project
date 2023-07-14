# 임시 네트워크 파이썬 코드 파일

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Active_Network(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_Network (Client).ui", self)  # UI 파일 로드
        self.setWindowTitle("네트워크 통신 (개발 0714버전)")
        self.setGeometry(570, 130, 970, 615)
        self.app_text_view.append('네트워크 윈도우창 텍스트뷰 테스트')

    def active_network(self):
        self.app_text_view.append('네트워크 윈도우창 텍스트뷰 테스트')


