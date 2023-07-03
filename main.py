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

import pyautogui
import time


class WebcamWindow(QMainWindow):


    def __init__(self):
        # timer
        self.start_time = 0
        self.elapse_time = 0

        # only one click
        self.is_LClicked = False
        self.is_RClicked = False
        self.is_MClicked = False
        self.is_DoubleClicked = False
        
        #################
        # screen_size = pyautogui.size()      # print(screen_size)       1920, 1080
        screen_size_x, screen_size_y = pyautogui.size()
        #################
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
        if not self.is_running:  # 웹캠 실행 플래그가 False이면 프레임 업데이트 중지
            return

        ret, frame = self.cap.read()  # 웹캠 프레임 읽기
        if ret:
            frame = cv2.flip(frame, 1)  # 웹캠 좌우 반전

            frame = self.hand_detector.find_hands(frame)
            lm_list, _ = self.hand_detector.find_positions(frame)

            # 각 손가락의 상태 ( True==펴짐, False==안펴짐)
            thumb_state = False  # 엄지
            index_state = False  # 검지
            middle_state = False  # 중지
            ring_state = False  # 약지
            pinky_state = False  # 소지

            # 마우스 이동 기능 추가
            if lm_list:
                # 손가락 펴짐 확인
                ################################
                thumb_state = lm_list[4][2] < lm_list[3][2] < lm_list[2][2] < lm_list[1][2]
                index_state = lm_list[8][2] < lm_list[7][2] < lm_list[6][2] < lm_list[5][2]
                middle_state = lm_list[12][2] < lm_list[11][2] < lm_list[10][2] < lm_list[9][2]
                ring_state = lm_list[16][2] < lm_list[15][2] < lm_list[14][2] < lm_list[13][2]
                pinky_state = lm_list[20][2] < lm_list[19][2] < lm_list[18][2] < lm_list[17][2]
                ################################
                print(thumb_state, index_state, middle_state, ring_state, pinky_state)

                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                middle_tip = lm_list[12]
                ring_tip = lm_list[16]
                pinky_tip = lm_list[20]

                thumb_index_distance = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)
                # print(thumb_index_distance)

                # 조건에 따라 마우스 기능 모듈을 호출 - 랜드마크 ( lm_list )
                # 마우스 커서 이동 - 모든 손가락이 펴짐
                if thumb_state and index_state and middle_state and ring_state and pinky_state:
                    self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                    self.is_LClicked = True
                    self.is_MClicked = True
                    self.is_RClicked = True
                    self.is_MClicked = True

                # 마우스 행동 해제 


                # 좌클릭 동작 수행 - 손가락 거리 조건
                if thumb_index_distance < 30 and self.is_LClicked:
                    self.start_time = time.time()
                    self.mouse_Left_PressEvent()
                    self.is_LClicked = False
                    
                elapse_time = time.time() - self.start_time

                if elapse_time > 1 and thumb_index_distance < 30:
                    self.mouse_Left_down()
                    if thumb_index_distance < 30:
                        self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())
                    if thumb_index_distance > 30:
                        self.mouse_Left_up()

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
    def mouse_MoveEvent(self, event, screen_size):
        MouseFunction.handle_mouse_move(self, event, screen_size)

    # 마우스 좌클릭 이벤트
    def mouse_Left_PressEvent(self):
        MouseFunction.handle_left_mouse_click(self)

    # 좌클릭 Drag를 위한 연속동작 down 이벤트
    def mouse_Left_down(self):
        MouseFunction.handle_mouse_press(self)

    def mouse_Left_up(self):
        MouseFunction.handle_mouse_up(self)

    # 마우스 우클릭 이벤트
    def mouse_Right_PressEvent(self):
        MouseFunction.handle_right_mouse_click(self)

    # 마우스 더블클릭 이벤트
    def mouse_Double_PressEvent(self):
        MouseFunction.handle_double_mouse_click(self)

    # 마우스 스크롤 이벤트
    def mouse_scroll_event(self, event):
        MouseFunction.handle_mouse_scroll(self, event)

    # 화면 확대 동작 수행
    # def mouse_zoom_in(self, event):
    #     MouseFunction.handle_mouse_zoom_in(self, event)

    # 화면 축소 동작 수행
    # def mouse_zoom_out(self, event):
    #     MouseFunction.handle_mouse_zoom_out(self, event)

    # 프로그램 종료 이벤트
    def closeEvent(self, event):
        self.stop_webcam()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebcamWindow()
    window.show()
    sys.exit(app.exec_())
