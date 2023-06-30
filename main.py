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
            # 마우스 이동 기능 추가
            if lm_list:
                # 마우스 커서 이동
                cursor_x = int(lm_list[8][1] * screen_size_x / 620) # x좌표 스케일링
                cursor_y = int(lm_list[8][2] * screen_size_y / 360) # y좌표 스케일링
                cursor_x = min(screen_size_x, max(0, cursor_x))     # x좌표 제한
                cursor_y = min(screen_size_y, max(0, cursor_y))     # y좌표 제한
                cursor = QCursor()
                # QCursor.setPos(cursor_x, cursor_y)
                self.cursor().setPos(cursor_x, cursor_y)

                print(cursor_x, cursor_y)
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                distance = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)

                # 마우스 행동 해제 - 손가락 거리 조건
                # distance 조건 잘못됨! (수정 필요!) #################################
                if distance < 30:
                    self.active_stop = True
                else:
                    self.active_stop = False

                # 좌클릭 동작 수행 - 손가락 거리 조건
                if distance < 30:
                    pyautogui.click()



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
    def mouse_MoveEvent(self, event):
        MouseFunction.handle_mouse_move(self, event)

    # 마우스 좌클릭 이벤트
    def mouse_Left_PressEvent(self, event):
        MouseFunction.handle_left_mouse_press(self, event)

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
