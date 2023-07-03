import cv2

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


cap = cv2.VideoCapture(0)

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
label = QLabel()
layout.addWidget(label)
window.setLayout(layout)
window.show()


def update_frame():
    ret, frame = cap.read()  # 웹캠 프레임 읽기
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        q_pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(q_pixmap)

timer = QTimer()
timer.timeout.connect(update_frame)
timer.start(30)  # 30ms마다 업데이트 (웹캠 프레임 속도에 맞게 조절)


app.exec_()
