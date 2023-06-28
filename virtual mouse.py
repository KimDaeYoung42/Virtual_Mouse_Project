# 손가락 위치정의
# WRIST = 0
# THUMB_CNC = 1
# THUMB_MCP = 2
# THUMB_IP = 3
# THUMB_TIP = 4     엄지
# INDEX_FINGER_MCP = 5
# INDEX_FINGER_PIP = 6
# INDEX_FINGER_DIP = 7
# INDEX_FINGER_TIP = 8      검지
# MIDDLE_FINGER_MCP = 9
# MIDDLE_FINGER_PIP = 10
# MIDDLE_FINGER_DIP = 11
# MIDDLE_FINGER_TIP = 12    중지
# RING_FINGER_MCP = 13
# RING_FINGER_PIP = 14
# RING_FINGER_DIP = 15
# RING_FINGER_TIP = 16      약지
# PINKY_MCP = 17
# PINKY_PIP = 18
# PINKY_DIP = 19
# PINKY_TIP = 20

import cv2
import mediapipe as mp
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import autopy

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

screen_width, screen_height = autopy.screen.size()

pre = ''
offset = 150

# webcam input
cap = cv2.VideoCapture(0)

