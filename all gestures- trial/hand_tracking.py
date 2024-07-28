import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def capture_hand_landmarks(cap):
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        return None, None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        result = hands.process(frame_rgb)
        return frame, result
