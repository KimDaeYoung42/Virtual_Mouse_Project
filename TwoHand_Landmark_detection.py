import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()

    results = hands.process(img)

    if results.multi_hand_landmarks:
        for res in results.multi_hand_landmarks:
            handedness = results.multi_handedness
            for hand in handedness:
                if hand.classification[0].label == "Left":  
                    # 왼손인 경우
                    print("왼손이 감지되었습니다.")
                elif hand.classification[0].label == "Right":  
                    # 오른손인 경우
                    print("오른손이 감지되었습니다.")


    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break