import mediapipe as mp

def recognize_gestures(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]

    # Calculate distances between landmarks
    distance_thumb_index = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    distance_index_middle = ((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)**0.5
    distance_middle_ring = ((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2)**0.5
    distance_ring_pinky = ((ring_tip.x - pinky_tip.x)**2 + (ring_tip.y - pinky_tip.y)**2)**0.5

    # Define thresholds
    threshold_open = 0.05
    threshold_click = 0.02

    # V gesture for mouse control (index and middle fingers spread, others folded)
    if distance_index_middle > threshold_open and distance_middle_ring < threshold_click and distance_ring_pinky < threshold_click:
        return 'v_shape'
    
    # Left click (V to middle finger to V gesture)
    if distance_index_middle < threshold_click and distance_ring_pinky < threshold_click:
        return 'left_click'
    
    # Right click (V to index finger to V gesture)
    if distance_middle_ring > threshold_open and distance_ring_pinky < threshold_click:
        return 'right_click'

    # Fist gesture for dragging
    if distance_thumb_index < threshold_click and distance_index_middle < threshold_click and distance_middle_ring < threshold_click and distance_ring_pinky < threshold_click:
        return 'fist'
    
    # Pinch gesture for volume/brightness control
    if distance_thumb_index < threshold_click and distance_index_middle > threshold_open and distance_middle_ring > threshold_open and distance_ring_pinky > threshold_open:
        return 'pinch'

    # Flick palm down for minimizing windows
    if all([landmark.y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y for landmark in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]]):
        return 'flick_down'

    # Flick palm up for restoring windows
    if all([landmark.y < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y for landmark in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]]):
        return 'flick_up'

    # Open start menu (pinch gesture with index and thumb)
    if distance_thumb_index < threshold_click:
        return 'open_start'

    return None
