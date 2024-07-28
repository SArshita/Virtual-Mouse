import cv2
import mediapipe as mp
from hand_tracking import capture_hand_landmarks, mp_drawing, mp_hands
from gesture_recognition import recognize_gestures
import actions

# Smoothing parameters
history_length = 5
mouse_positions = []

def smooth_coordinates(new_x, new_y):
    mouse_positions.append((new_x, new_y))
    if len(mouse_positions) > history_length:
        mouse_positions.pop(0)
    avg_x = sum([pos[0] for pos in mouse_positions]) // len(mouse_positions)
    avg_y = sum([pos[1] for pos in mouse_positions]) // len(mouse_positions)
    return avg_x, avg_y

def main():
    cap = cv2.VideoCapture(0)
    is_dragging = False

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                # Flip the frame horizontally to create a mirror image
                frame = cv2.flip(frame, 1)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(frame_rgb)

                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        # Draw hand landmarks
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        # Recognize gestures and perform actions
                        gesture = recognize_gestures(hand_landmarks)
                        print(f"Gesture detected: {gesture}")

                        if gesture == 'v_shape':
                            x = int((1 - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) * frame.shape[1])
                            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])
                            smooth_x, smooth_y = smooth_coordinates(x, y)
                            actions.move_mouse(smooth_x, smooth_y)
                        elif gesture == 'left_click':
                            actions.click_left()
                        elif gesture == 'right_click':
                            actions.click_right()
                        elif gesture == 'fist':
                            if not is_dragging:
                                actions.drag()
                                is_dragging = True
                            x = int((1 - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) * frame.shape[1])
                            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])
                            smooth_x, smooth_y = smooth_coordinates(x, y)
                            actions.move_mouse(smooth_x, smooth_y)
                        elif gesture == 'pinch':
                            thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                            index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                            if thumb_tip_y < index_tip_y:
                                actions.control_volume(increase=True)
                            else:
                                actions.control_volume(increase=False)
                        elif gesture == 'flick_down':
                            actions.minimize_windows()
                        elif gesture == 'flick_up':
                            actions.restore_windows()
                        elif gesture == 'open_start':
                            actions.open_start_menu()

                if is_dragging and gesture != 'fist':
                    actions.release_drag()
                    is_dragging = False

                cv2.imshow('Virtual Mouse', frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
