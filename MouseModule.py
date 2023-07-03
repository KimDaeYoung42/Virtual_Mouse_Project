import cv2
import math
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QCursor

import autopy
import pyautogui
from HandTrackingModule import HandDetector

class MouseFunction:
    def __init__(self):
        self.screen_size = autopy.screen.size()
        self.screen_size_x, self.screen_size_y = self.screen_size

    active_stop = False # 임시


    # 마우스 이동 이밴트 처리
    def handle_mouse_move(self, event, screen_size):
        if MouseFunction.active_stop:
            return

        size_x, size_y = screen_size
        # cursor_pos = event.pos()
        cursor_x = int(event[9][1] * size_x / 620)          # x좌표 스케일링
        cursor_y = int(event[9][2] * size_y / 360)          # y좌표 스케일링
        cursor_x = min(size_x - 1, max(0, cursor_x))        # x좌표 제한
        cursor_y = min(size_y - 1, max(0, cursor_y))        # y좌표 제한
        cursor = QCursor()
        # QCursor.setPos(cursor_x, cursor_y)
        self.cursor().setPos(cursor_x, cursor_y)

    # 마우스 좌클릭 이벤트 처리 - 기능 추가 필요!
    def handle_left_mouse_press(self, event):
        self.text_view.append('마우스 좌클릭 이벤트 감지')
        # if MouseFunction.active_stop:
        #    return

        pyautogui.click()  # 파일 선택 혹은 웹 브라우저 창 선택 등의 동작 수행



    # 마우스 스크롤 이벤트 처리 - 기능 추가 필요!
    def handle_mouse_scroll(self, event):
        self.text_view.append('마우스 스크롤 이벤트 감지')
        if MouseFunction.active_stop:
            return

        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

    # 화면 확대 동작 수행 - 기능 추가 필요!
    def handle_mouse_zoom_in(self, event):
        self.text_view.append('마우스 확대 이벤트 감지')
        if MouseFunction.active_stop:
            return

        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width + 10, current_height + 10)

    # 화면 축소 동작 수행 - 기능 추가 필요!
    def handle_mouse_zoom_out(self, event):
        self.text_view.append('마우스 축소 이벤트 감지')
        if MouseFunction.active_stop:
            return

        current_width = self.Webcam_label.width()
        current_height = self.Webcam_label.height()
        self.Webcam_label.resize(current_width + 10, current_height + 10)


    # 윈도우 창 이동 (드래그 앤 무브) - 기능 추가 필요!
    def handle_mouse_move_window(self, event):
        self.text_view.append('마우스 드래그 앤 무브 이벤트 감지')
        if MouseFunction.active_stop:
            return
        # 윈도우 창 이동 코드 작성 필요
        # ㅇㅇ







