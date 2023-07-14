# App.py : 메인 프로그램.

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor
from PyQt5.QtCore import Qt, QProcess

from App_Active import Active_Webcam
from Network_Con import Active_Network
from App_Help import Active_Help

import autopy
import icon_toolbar                                 # 삭제 금지! 비활성화상태라도 활성화되어있음!
import pyautogui

#################
# 화면 크기 설정
screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
screen_size_x, screen_size_y = screen_size
#################

class App_Control(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_App_Main.ui", self)  # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램 (개발 0714버전)")
        self.setGeometry(100, 100, 440, 330)

        # 인스턴스 생성
        self.app_active = Active_Webcam()           # 인스턴스 생성.
        self.network_active = Active_Network()
        self.help_active = Active_Help()

        # 초기화 (프로그램 중복실행 방지)
        self.cap_count = 0
        self.network_count = 0

        # 버튼 클릭 이벤트 연결
        self.Button_WebCam_Start.clicked.connect(self.start_webcam)
        self.Button_WebCam_Stop.clicked.connect(self.stop_webcam)
        self.Button_Network_Start.clicked.connect(self.start_network)
        self.Button_Network_Stop.clicked.connect(self.stop_network)
        self.Button_Exit.clicked.connect(self.stop_program)

        # 상단 UI 버튼 이벤트 연결
        self.action_WebCam_Start.triggered.connect(self.start_webcam)
        self.action_WebCam_Stop.triggered.connect(self.stop_webcam)
        self.action_NetWork_ON.triggered.connect(self.start_network)
        self.action_NetWork_OFF.triggered.connect(self.stop_network)

        self.action_Capture.triggered.connect(self.capture_tool)
        self.action_help.triggered.connect(self.help_button)

    # 웹캠 UI 버튼
    def start_webcam(self):
        if self.cap_count == 0:
            self.cap_count += 1
            self.app_text_view.append('App : 웹캠 실행 준비 완료')
            self.app_active.show()
            self.app_text_view.append('App : 웹캠이 실행됩니다')
            self.app_active.active_webcam()
        else:
            self.app_text_view.append('App : 웹캠이 이미 실행되고 있습니다.')

    def stop_webcam(self):
        if not self.cap_count == 0:
            self.cap_count = 0
            self.app_text_view.append('App : 웹캠 종료 중...')
            self.app_text_view.append('App : 웹캠이 종료됩니다')

            self.app_active.close()
        else:
            self.app_text_view.append('App : 웹캠이 이미 종료되었습니다.')

        # if self.cap is not None:
        #     self.cap.release()
        #     self.text_view.append('경고 : 웹캠이 정상적으로 작동되지 않습니다.')
        #     self.cap = None
        # self.timer.stop()
        # # self.label.clear() # <-- 종료
        #
        # self.is_running = False         # 웹캠 실행 플래그를 False로 설정

    # 네트워크 UI 버튼
    def start_network(self):
        if self.network_count == 0:
            self.network_count += 1
            self.app_text_view.append('App : 네트워크 실행 준비 완료')
            self.network_active.show()
            self.app_text_view.append('App : 네트워크 기능이 실행됩니다.')
        else:
            self.app_text_view.append('App : 네트워크 기능이 이미 실행 중입니다.')

    def stop_network(self):
        if not self.network_count == 0:
            self.network_count = 0
            self.app_text_view.append('App : 네트워크 기능이 종료됩니다.')
            self.network_active.close()
        else:
            self.app_text_view.append('App : 네트워크 기능이 이미 종료되었습니다.')

    # 종료 UI 버튼
    def stop_program(self):
        self.app_text_view.append('App : 프로그램이 종료됩니다')
        QApplication.quit()

    # 상단 UI - toolbar 버튼
    def capture_tool(self):
        capture_tool_path = "C:\windows\system32\SnippingTool.exe"  # 윈도우 캡처 도구 실행 파일 경로

        capture_process = QProcess(self)
        capture_process.startDetached(capture_tool_path)

    def help_button(self):
        self.app_text_view.append('App : Help!')
        self.help_active.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App_Control()
    window.show()
    sys.exit(app.exec_())

