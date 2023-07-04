# App_Active.py : 마우스, 키보드 기능 코드 1번.

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

import autopy
import pyautogui

#################
# 화면 크기 설정
screen_size = autopy.screen.size()                  # print(screen_size) 1920, 1080 <- 모니터 1대만 사용시 기준
screen_size_x, screen_size_y = screen_size
#################

class Active_Webcam(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("App_WebCam.ui", self)               # UI 파일 로드
        self.setWindowTitle("개발자 모드 - 웹캠 표현 (개발 0704버전)")
        # self.setWindowFlag(Qt.FramelessWindowHint) # 윈도우창 프레임 숨기기

        self.text_view.append('웹캠 실행 중...')

        self.cap = None                             # 웹캠 객체
        self.hand_detector = HandDetector()         # 인스턴스 생성.

        self.is_running = False  # 웹캠 실행 여부 flag

        # 마우스 행동 해제
        self.active_stop = False

    def active_webcam(self):
        self.cap = cv2.VideoCapture(0)  # 웹캠 번호 (0은 기본 웹캠)

        self.is_running = True          # 웹캠 실행 플래그를 True로 설정

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)            # 30m/s마다 업데이트 (웹캠 프레임 속도에 맞게 조절)

    def update_frame(self):
        if not self.is_running:  # 웹캠 실행 플래그가 False이면 프레임 업데이트 중지
            self.text_view.append('에러 : 웹캠이 정상적으로 실행되지 않았습니다')
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

            #
            if lm_list:
                # 손가락 펴짐 상태의 조건 (좌클릭 동작 수행 - 손가락 거리 조건)
                if lm_list[4][2] < lm_list[3][2]:
                    if lm_list[3][2] < lm_list[2][2]:
                        if lm_list[2][2] < lm_list[1][2]:
                            thumb_state = True

                if lm_list[8][2] < lm_list[7][2]:
                    if lm_list[7][2] < lm_list[6][2]:
                        if lm_list[6][2] < lm_list[5][2]:
                            index_state = True

                if lm_list[12][2] < lm_list[11][2]:
                    if lm_list[11][2] < lm_list[10][2]:
                        if lm_list[10][2] < lm_list[9][2]:
                            middle_state = True

                if lm_list[16][2] < lm_list[15][2]:
                    if lm_list[15][2] < lm_list[14][2]:
                        if lm_list[14][2] < lm_list[13][2]:
                            ring_state = True

                if lm_list[20][2] < lm_list[19][2]:
                    if lm_list[19][2] < lm_list[18][2]:
                        if lm_list[18][2] < lm_list[17][2]:
                            pinky_state = True

                print(thumb_state, index_state, middle_state, ring_state, pinky_state)      # 손가락 펴짐상태 출력

                ################################

                # 일반 행동 해제 (손 모양이 주먹일 경우) <- 오류 있음
                if not (thumb_state or index_state or middle_state or ring_state or pinky_state):
                    self.active_stop() # 웹캠 실행 시 - 손이 인식이 안되면 꺼지는 오류 있음.
                    self.text_view.append('기능 : 일반 행동 해제')

                # 마우스 커서 이동 (모든 손가락이 펴진 상태인 True일때)
                if thumb_state and index_state and middle_state and ring_state and pinky_state:
                    self.mouse_MoveEvent(event=lm_list, screen_size=pyautogui.size())

                # 마우스 좌클릭 조건
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                distance_Left = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)

                if distance_Left < 30:
                    self.mouse_Left_ClickEvent()

                # 양손 트래킹 기반 확대/축소 수행
                # if lm_list and len(lm_list) >= 9:
                #      left_thumb_tip = lm_list[4]
                #      left_index_tip = lm_list[8]
                #      right_thumb_tip = lm_list[12]
                #      right_index_tip = lm_list[16]
                #      print(left_thumb_tip)
                #
                #      left_distance = math.sqrt(
                #          (left_thumb_tip[0] - left_index_tip[0]) ** 2 + (left_thumb_tip[1] - left_index_tip[1]) ** 2)
                #      right_distance = math.sqrt(
                #          (right_thumb_tip[0] - right_index_tip[0]) ** 2 + (right_thumb_tip[1] - right_index_tip[1]) ** 2)
                #
                #      if left_distance > 15 and right_distance > 15:
                #          self.text_view.append('스크롤 확대 이벤트 감지')
                #          pyautogui.scroll(20)
                #      elif left_distance < 10 and right_distance < 10:
                #          self.text_view.append('스크롤 축소 이벤트 감지')
                #          pyautogui.scroll(-20)

                # 키보드 기능 화상키보드 켜기 (새끼손가락만)
                if not (thumb_state and index_state and middle_state and ring_state) and pinky_state:
                    self.keyboard_on_Event()

            # 프레임 화면에 출력
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.Webcam_label.setPixmap(q_pixmap)

    ## 공통 기능 ##
    # 행동 해제 이벤트
    def active_stop(self):
        self.text_view.append('기능 : 행동 해제 이벤트 감지')

    ### 마우스 기능 파트 (MouseModule.py에서 핸들 주고받아옴) ###
    # 마우스 기능 분기 적용 필요함! (단, 행동 해제 이벤트는 상위 이벤트임 )
    # 1. 마우스 이동 이벤트
    def mouse_MoveEvent(self, event, screen_size):
        MouseFunction.handle_mouse_move(self, event, screen_size)

    # 2. 마우스 좌클릭 관련
    # 2.1 마우스 좌클릭 이벤트 (1번 좌클릭 / 좌 프레스(계속 누르는) )
    def mouse_Left_ClickEvent(self):
        MouseFunction.handle_left_mouse_click(self)
        self.text_view.append('기능 : 마우스 좌클릭 이벤트 감지')

    # 2.2 마우스 좌 더블클릭 이벤트 (2번 좌클릭)

    # 2.3 마우스 좌클릭 후 드래그 이벤트

    # 2.4 마우스 좌클릭 후 끌어서 놓기 이벤트 (파일 이동 / 클릭 앤 무브)

    # 3. 마우스 우클릭 관련
    # 3.1 마우스 우클릭 이벤트 (1번 우클릭 / 우 프레스 (계속 누르는) )

    # 4. 마우스 스크롤 관련
    # 4.1 마우스 스크롤 클릭 이벤트

    # 4.2 마우스 스크롤 이벤트
    def mouse_scroll_event(self, event):
        MouseFunction.handle_mouse_scroll(self, event)
        self.text_view.append('기능 : 마우스 스크롤 이벤트 감지')

    # 4.2.1 화면 스크롤 - 확대 동작 수행
    def mouse_zoom_in(self, event):
        MouseFunction.handle_mouse_zoom_in(self, event)
        self.text_view.append('기능 : 마우스 확대 이벤트 감지')

    # 4.2.2 화면 스크롤 - 축소 동작 수행
    def mouse_zoom_out(self, event):
        MouseFunction.handle_mouse_zoom_out(self, event)
        self.text_view.append('기능 : 마우스 축소 이벤트 감지')

    ### 키보드 기능 파트 (MouseModule.py에서 핸들 주고받아옴) ###
    # 윈도우 화상키보드 ON
    def keyboard_on_Event(self):
        keyboard_process = subprocess.Popen('osk.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.text_view.append('기능 : 키보드 이벤트 감지')
        # 화상 키보드 선행설정 - 옵션 - 화상키보드 사용방식 중 가리켜서 입력 3초 기준
        # notepad_process = subprocess.Popen('notepad.exe', shell=True)

        if MouseFunction.active_stop:
            keyboard_process.terminate()    # 화상 키보드 종료
            return

