import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor

import cv2
import mediapipe as mp
import math
from HandTrackingModule import HandDetector
from MouseModule import MouseFunction

import autopy
import pyautogui

#################
screen_size = autopy.screen.size()      # print(screen_size)       1920, 1080
screen_size_x, screen_size_y = screen_size
#################

class WebcamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Main_testui.ui", self)  # UI 파일 로드
        self.setWindowTitle("Webcam Window")

        self.cap = None  # 웹캠 객체
        self.hand_detector = HandDetector()

        # 버튼 클릭 이벤트 연결
        self.Button_WebCam_Start.clicked.connect(self.start_webcam)
        self.Button_WebCam_Stop.clicked.connect(self.stop_webcam)

        self.is_running = False  # 웹캠 실행 여부 flag

        # 마우스 행동 해제
        self.active_stop = False

        # 마우스 스크롤 이벤트 연결 (추후 UI 내에서 스크롤 동작 기능)
        # self.Webcam_label.wheelEvent = self.zoom_event

    def start_webcam(self):
        self.text_view.append('웹캠이 실행됩니다')

        self.cap = cv2.VideoCapture(0)  # 웹캠 번호 (0은 기본 웹캠)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)            # 30m/s마다 업데이트 (웹캠 프레임 속도에 맞게 조절)

        self.is_running = True          # 웹캠 실행 플래그를 True로 설정

    def stop_webcam(self):
        self.text_view.append('웹캠이 종료됩니다')

        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.timer.stop()
        self.label.clear()

        self.is_running = False         # 웹캠 실행 플래그를 False로 설정

    def update_frame(self):
        if not self.is_running:         # 웹캠 실행 플래그가 False이면 프레임 업데이트 중지
            return

        ret, frame = self.cap.read()    # 웹캠 프레임 읽기
        if ret:
            frame = cv2.flip(frame, 1)  # 웹캠 좌우 반전

            frame = self.hand_detector.find_hands(frame)
            lm_list, _ = self.hand_detector.find_positions(frame)

            ################################ 핸드 모션 기준 추가하는 곳

            ################################
            # 각 손가락의 상태 ( True==펴짐, False==안펴짐)
            thumb_state = False     # 엄지
            index_state = False     # 검지
            middle_state = False    # 중지
            ring_state = False      # 약지
            pinky_state = False     # 소지

            if lm_list[4][1] > lm_list[3][1]:
                if lm_list[3][1] > lm_list[2][1]:
                    if lm_list[2][1] > lm_list[1][1]:
                        thumb_state = True
            
            if lm_list[8][1] > lm_list[7][1]:
                if lm_list[7][1] > lm_list[6][1]:
                    if lm_list[6][1] > lm_list[5][1]:
                        index_state = True
            
            if lm_list[12][1] > lm_list[11][1]:
                if lm_list[11][1] > lm_list[10][1]:
                    if lm_list[10][1] > lm_list[9][1]:
                        middle_state = True

            if lm_list[16][1] > lm_list[15][1]:
                if lm_list[15][1] > lm_list[14][1]:
                    if lm_list[14][1] > lm_list[13][1]:
                        ring_state = True
            
            if lm_list[20][1] > lm_list[19][1]:
                if lm_list[19][1] > lm_list[18][1]:
                    if lm_list[18][1] > lm_list[17][1]:
                        pinky_state = True
            ################################

            if lm_list:
                
                # 마우스 커서 이동
                if thumb_state and index_state and middle_state and ring_state and pinky_state:
                    self.mouse_MoveEvent(lm_list)
                

                



            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label.setPixmap(q_pixmap)

    ## 공통 기능 ##
    # 행동 해제 이벤트
    def active_stop(self, is_first):
        self.text_view.append('행동 해제 이벤트 감지')
        self.active_stop = is_first


    ### 마우스 기능 파트 (MouseModule.py에서 핸들 주고받아옴) ###
    # 마우스 기능 분기 적용 필요함! (단, 행동 해제 이벤트는 상위 이벤트임 )
    # 마우스 이동 이밴트
    def mouse_MoveEvent(self, lm_list):
        MouseFunction.handle_mouse_move(self, lm_list)

    # 마우스 좌클릭 이벤트
    def mouse_Left_PressEvent(self, lm_list):
        MouseFunction.handle_left_mouse_press(self, lm_list)

    # 마우스 우클릭 이벤트
    # 마우스 ?클릭 이벤트

    # 마우스 스크롤 이벤트
    def mouse_scroll_event(self, event):
        MouseFunction.handle_mouse_scroll(self, event)

    # 화면 확대 동작 수행
    def mouse_zoom_in(self, event):
        MouseFunction.handle_mouse_zoom_in(self, event)

    # 화면 축소 동작 수행
    def mouse_zoom_out(self, event):
        MouseFunction.handle_mouse_zoom_out(self, event)

    # 윈도우 창 이동 (드래그 앤 무브)
    def handle_mouse_move_window(self, dx, dy, event):
        MouseFunction.handle_mouse_move_window(self, event)



app = QApplication(sys.argv)
window = WebcamWindow()
window.show()
sys.exit(app.exec_())
