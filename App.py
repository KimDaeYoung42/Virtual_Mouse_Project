# App.py : 메인 프로그램.

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor

import cv2
import mediapipe as mp
import math
from HandTrackingModule import HandDetector
from MouseModule import MouseFunction
from App_Active import Active_Webcam

import autopy
import pyautogui

#################
# 화면 크기 설정
screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
screen_size_x, screen_size_y = screen_size
#################
# QMainWindow

class App_Control(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI_App.ui", self)  # UI 파일 로드
        self.setWindowTitle("가상 인터페이스 프로그램 (개발 0705버전)")

        self.cap = None                             # 웹캠 객체
        self.app_active = Active_Webcam()           # 인스턴스 생성.

        # 버튼 클릭 이벤트 연결
        # self.Button_Mouse.clicked.connect(self.start_webcam)      # 마우스 기능 활성화 (아직 미완)
        # self.Button_Keyboard.clicked.connect(self.start_webcam)   # 키보드 기능 활성화 (아직 미완)

        self.Button_WebCam_Start.clicked.connect(self.start_webcam)
        self.Button_WebCam_Stop.clicked.connect(self.stop_webcam)
        self.Button_Exit.clicked.connect(self.stop_program)

        # 마우스 스크롤 이벤트 연결 (추후 UI 내에서 스크롤 동작 기능)
        # self.setMouseTracking(True)
        # self.Webcam_label.wheelEvent = self.zoom_event

    def start_webcam(self):
        self.app_text_view.append('App : 웹캠 실행 준비 완료')
        self.app_active.show()
        self.app_text_view.append('App : 웹캠이 실행됩니다')
        self.app_active.active_webcam()

    def stop_webcam(self):
        self.app_text_view.append('App : 웹캠 종료 중...')
        self.app_text_view.append('App : 웹캠이 종료됩니다')

        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.timer.stop()
        # self.label.clear() # <-- 종료

        self.is_running = False         # 웹캠 실행 플래그를 False로 설정

    def stop_program(self):
        self.app_text_view.append('App : 프로그램이 종료됩니다')
        self.label.clear()

        self.is_running = False  # 웹캠 실행 플래그를 False로 설정


    #################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App_Control()
    window.show()
    sys.exit(app.exec_())