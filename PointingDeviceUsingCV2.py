import cv2
import mediapipe as mp
import pyautogui
import numpy as np
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

prev_x, prev_y = 0, 0
smoothening = 7

def fingers_up(hand_landmarks):
    """
    Returns a list of 5 elements: 1 if finger is up, else 0
    """
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def is_reverse_palm(hand_landmarks):
    """
    Detect reverse palm: if wrist (0) is higher than middle finger MCP (9)
    """
    return hand_landmarks.landmark[0].y < hand_landmarks.landmark[9].y

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror image for display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = img.shape

        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Flip x for mirrored behavior
        x_index = (1 - hand_landmarks.landmark[8].x) * w
        y_index = hand_landmarks.landmark[8].y * h

        # Map to screen size with smoothing
        screen_x = np.interp(x_index, [0, w], [0, screen_width])
        screen_y = np.interp(y_index, [0, h], [0, screen_height])
        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        fingers = fingers_up(hand_landmarks)

        # Left click: All fingers up
        if fingers == [1, 1, 1, 1, 1]:
            pyautogui.doubleClick()

            cv2.putText(img, "Left Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Right click: Reverse palm
        elif is_reverse_palm(hand_landmarks):
            pyautogui.click(button='right')
            cv2.putText(img, "Right Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Hand Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
