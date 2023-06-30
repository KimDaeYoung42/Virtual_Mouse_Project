import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCursor

import cv2
import mediapipe as mp
import math
from HandTrackingModule import HandDetector

import pyautogui
import time

#################
screen_size = pyautogui.size()
# print(screen_size)       1920, 1080
# screen_size_x, screen_size_y = autopy.screen.size()
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

        self.is_running = False  # 웹캠 실행 여부를 나타내는 플래그

        # 마우스 스크롤 이벤트 연결
        self.Webcam_label.wheelEvent = self.scroll_event
        self.setMouseTracking(True)  # 마우스 이벤트 추적을 위해 설정

        # 마우스 드래그 앤 무브 변수 초기화
        self.dragging = False
        self.prev_x = 0
        self.prev_y = 0

        # 마우스 행동 해제
        self.acive_stop = False

    def start_webcam(self):
        self.text_view.append('웹캠이 실행됩니다')

        self.cap = cv2.VideoCapture(0)  # 웹캠 번호 (0은 기본 웹캠)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)            # 30ms마다 업데이트 (웹캠 프레임 속도에 맞게 조절)

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


            # 마우스 이동 기능 추가
            if lm_list: 
                action = '?'
                # 마우스 커서 이동 - 모든 손가락 펴짐
                if thumb_state and index_state and middle_state and ring_state and pinky_state:
                    action ='move'
                    cursor_x = int(lm_list[8][1] * screen_size_x / 620) # x좌표 스케일링
                    cursor_y = int(lm_list[8][2] * screen_size_y / 360) # y좌표 스케일링
                    cursor_x = min(screen_size_x, max(0, cursor_x))     # x좌표 제한
                    cursor_y = min(screen_size_y, max(0, cursor_y))     # y좌표 제한
                    cursor = QCursor()
                    # QCursor.setPos(cursor_x, cursor_y)
                    self.cursor().setPos(cursor_x, cursor_y)

                    # print(cursor_x, cursor_y)

                index_tip = lm_list[8]
                middle_tip = lm_list[12]
                # distance = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)
                distance = abs(index_tip[0] - middle_tip[0])
                self.text_view.append(distance)

                # 마우스 행동 해제 - 모든 손가락이 접힘
                if not thumb_state and not index_state and not middle_state and not ring_state and not pinky_state:
                    action ='none'
                    self.acive_stop = True
                else:
                    self.acive_stop = False

                # 좌클릭 동작 수행 - 검지와 중지가 펴짐, 손가락 거리 조건
                if index_state and middle_state and not thumb_state and not ring_state and not pinky_state and distance < 30:
                    action = 'Lclick'
                    pyautogui.click()
                    start_time = time.time()
                    self.acive_stop = False

                # 좌클릭 이후 2초가 지난 상태 유지 -> 드래그
                elapse_time = time.time() - start_time 
                if action == 'Lclick' and elapse_time > 2:
                    pyautogui.mouseDown(button='left')  # 드래그 상태
                    # 움직임 적용
                    if distance < 30:
                        cursor_x = int(lm_list[8][1] * screen_size_x / 620) # x좌표 스케일링
                        cursor_y = int(lm_list[8][2] * screen_size_y / 360) # y좌표 스케일링
                        cursor_x = min(screen_size_x, max(0, cursor_x))     # x좌표 제한
                        cursor_y = min(screen_size_y, max(0, cursor_y))     # y좌표 제한
                        cursor = QCursor()
                        # QCursor.setPos(cursor_x, cursor_y)
                        self.cursor().setPos(cursor_x, cursor_y)
                    elif distance > 30:
                        pyautogui.mouseUp(button='left')
                        elapse_time = 0

                # 우클릭 동작 수행

                # 마우스 스크롤 동작 수행 - 손가락 거리 조건
                # if distance > 50:
                #    self.zoom_in()
                # elif distance < 30:
                #    self.zoom_out()

                # 마우스 줌 인 & 줌 아웃 (핸드 모션 기준) - 손가락 거리 조건
                # if distance < 30:
                #     self.dragging = True
                #     self.prev_x, self.prev_y = thumb_tip[0], thumb_tip[1]
                # elif self.dragging:
                #     dx, dy = thumb_tip[0] - self.prev_x, thumb_tip[1] - self.prev_y
                #     self.move_window(dx, dy)
                #     self.prev_x, self.prev_y = thumb_tip[0], thumb_tip[1]
                # else:
                #     self.dragging = False

            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label.setPixmap(q_pixmap)

    ### 마우스 기능 파트 ###
    # def acive_stop(self, event):



    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        if self.acive_stop:
            return

        cursor_pos = event.pos()
        cursor_x = cursor_pos.x()
        cursor_y = cursor_pos.y()
        cursor_x = min(screen_size_x - 1, max(0, cursor_x))  # x좌표 제한
        cursor_y = min(screen_size_y - 1, max(0, cursor_y))  # y좌표 제한
        cursor = QCursor()
        # QCursor.setPos(cursor_x, cursor_y)
        self.cursor().setPos(cursor_x, cursor_y)

    # 마우스 좌클릭 이벤트 처리
    def mousePressEvent(self, event):
        if self.acive_stop:
            return

        if event.button() == Qt.LeftButton:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = self.hand_detector.find_hands(frame)
                lm_list, _ = self.hand_detector.find_positions(frame)

                if lm_list:
                    # 검지와 중지 좌표 가져오기
                    index_tip = lm_list[8]
                    middle_tip = lm_list[12]
                    # 검지와 중지의 거리 계산
                    # distance = math.sqrt((index_tip[1] - index_tip[1]) ** 2 + (middle_tip[2] - middle_tip[2]) ** 2)
                    distance = abs(index_tip[0] - middle_tip[0])

            # 일정 거리 이하로 접근했을 때 좌클릭 이벤트 발생
            if distance < 30:
                pyautogui.click()        # 파일 선택 혹은 웹 브라우저 창 선택 등의 동작 수행


    # 마우스 드래그 앤 드롭
    def DragAndDrop_event(self, event):
        if self.acive_stop:
            return


    # 마우스 스크롤 이벤트 처리
    def scroll_event(self, event):
        if self.acive_stop:
            return

        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

    # 윈도우 창 이동 (드래그 앤 무브)
    def move_window(self, dx, dy):
        pos_x = self.pos().x() + dx
        pos_y = self.pos().y() + dy
        self.move(pos_x, pos_y)

    # 화면 확대 동작 수행
    def zoom_in(self):
        # 화면 확대 동작 수행
        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width + 10, current_height + 10)

    # 화면 축소 동작 수행
    def zoom_out(self):
        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width - 10, current_height - 10)

app = QApplication(sys.argv)
window = WebcamWindow()
window.show()
sys.exit(app.exec_())
