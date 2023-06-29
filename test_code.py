import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import autopy
import time

actions = ['none', 'move', 'Lclick', 'Rclick', 'doubleclick']
seq_length = 30

model = load_model('models/model.h5')

screen_size = autopy.screen.size()
# print(screen_size)       1920, 1080
screen_size_x, screen_size_y = autopy.screen.size()

# only one click
is_Lclicked = True
is_RClicked = True
is_DoubleClicked = True

# timer
start_time = 0

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

seq = []
action_seq = []

while cap.isOpened():
    ret, img = cap.read()

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_height, img_width, _ = img.shape

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 4))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

            # Compute angles between joints
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
            v = v2 - v1 # [20, 3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

            angle = np.degrees(angle) # Convert radian to degree

            d = np.concatenate([joint.flatten(), angle])

            seq.append(d)

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

            if len(seq) < seq_length:
                continue

            input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)

            y_pred = model.predict(input_data).squeeze()

            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]

            if conf < 0.9:
                continue

            action = actions[i_pred]
            action_seq.append(action)

            if len(action_seq) < 3:
                continue

            index_middle_distance = abs(joint[12][0] - joint[8][0]) * 100
            # print(index_middle_distance)

            this_action = '?'

            # action이 3개 연속일 때
            if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                this_action = action

            cv2.putText(img, f'{this_action.upper()}', org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

            # 손의 위치를 추적해 마우스 커서의 위치를 바꾼다
            if this_action == 'move':

                is_Lclicked = True
                is_RClicked = True
                is_DoubleClicked = True

                # 손목의 위치 가져오기
                x =  joint[9][0]
                y =  joint[9][1]

                # 마우스 커서 이동
                normalized_x = screen_size_x * x
                normalized_y = screen_size_y * y

                if normalized_x > screen_size_x:
                    continue
                elif normalized_y > screen_size_y:
                    continue
                
                autopy.mouse.move(normalized_x, normalized_y)
            
            # 마우스 좌클릭
            if this_action == 'Lclick' and is_Lclicked == True:
                start_time = time.time()
                is_RClicked = True
                is_DoubleClicked = True

                autopy.mouse.click()

                is_Lclicked = False

            elapse_time = time.time() - start_time

            # 좌클릭 2초 지속시 드래그
            if this_action == 'Lclick' and elapse_time >= 2:
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=True)
                
                while index_middle_distance < 5:
                    x = joint[9][0]
                    y = joint[9][1]

                    # 마우스 커서 이동
                    normalized_x = screen_size_x * x
                    normalized_y = screen_size_y * y

                    if normalized_x > screen_size_x:
                        continue
                    elif normalized_y > screen_size_y:
                        continue
                
                    autopy.mouse.move(normalized_x, normalized_y)

                    if index_middle_distance > 5:
                        autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=False)
                        break

                elapse_time = 0

            # 마우스 우클릭
            if this_action == 'Rclick' and is_RClicked == True:

                is_Lclicked = True
                is_DoubleClicked = True

                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                is_RClicked = False
            
            # L버튼 더블클릭
            if this_action =='doubleclick' and is_DoubleClicked == True:

                is_Lclicked = True
                is_RClicked = True

                autopy.mouse.click()
                time.sleep(0.1)
                autopy.mouse.click()
                is_DoubleClicked = False

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
