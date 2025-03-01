import mediapipe as mp
import cv2
import pyautogui

mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
Pose = mpPose.Pose()

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

shoot = False
jump = False
forward = False
backward = False
moving_left=False
moving_right=False
reload=False
spike_controls=False
stop=False

def reset_controls():
    pyautogui.keyUp(5)
    pyautogui.keyUp("space")
    pyautogui.keyUp("w")
    pyautogui.keyUp("s")
    pyautogui.keyUp("a")
    pyautogui.keyUp("d")
    pyautogui.keyUp("r")
    pyautogui.keyUp(4)


while True:
    success, img = cap.read()
    if not success:
        print("Camera not found!")
        break

    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_pose = Pose.process(imgrgb)
    results_hands = hands.process(imgrgb)

    # Initialize pose landmarks
    right_wrist_y = None
    right_index_y = None
    left_wrist_y = None
    head_y = None
    right_hand_open = False
    left_hand_open = False
    left_shoulder_y = None
    right_shoulder_y = None
    right_elbow_y = None
    left_elbow_y = None

    if results_pose.pose_landmarks:
        mpDraw.draw_landmarks(img, results_pose.pose_landmarks, mpPose.POSE_CONNECTIONS)
        h, w, c = img.shape  # Get image dimensions

        for id, lm in enumerate(results_pose.pose_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)

            if id == 16:  # Right wrist
                right_wrist_y = cy
            elif id == 18:  # Right index finger
                right_index_y = cy
            elif id == 15:  # Left wrist
                left_wrist_y = cy
            elif id == 0:  # Head
                head_y = cy
            elif id == 11:  # Left Shoulder
                left_shoulder_y = cy
            elif id == 12:  # Right Shoulder
                right_shoulder_y = cy
            if id == 14:  # Right Elbow
                right_elbow_y = cy
            elif id == 13:  # Left Elbow
                left_elbow_y = cy

            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    # Process hands (finger gestures)
    if results_hands.multi_hand_landmarks:
        for handLms in results_hands.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            h, w, c = img.shape
            landmarks = handLms.landmark

            wrist_y = landmarks[0].y * h
            index_tip_y = landmarks[8].y * h
            middle_tip_y = landmarks[12].y * h
            ring_tip_y = landmarks[16].y * h
            pinky_tip_y = landmarks[20].y * h

            hand_side = "right" if landmarks[0].x > 0.5 else "left"

            # Determine if hand is open (all fingers extended above wrist)
            is_hand_open = (
                    index_tip_y < wrist_y and middle_tip_y < wrist_y and
                    ring_tip_y < wrist_y and pinky_tip_y < wrist_y
            )

            # Moving Forward (Closed Fist - All fingers below wrist)
            if (index_tip_y > wrist_y and middle_tip_y > wrist_y and
                ring_tip_y > wrist_y and pinky_tip_y > wrist_y):
                if not forward:
                    pyautogui.keyDown("w")
                    forward = True
            else:
                if forward:
                    pyautogui.keyUp("w")
                    forward = False

            # Moving Backward (Open Palm - All fingers above wrist)
            if (index_tip_y < wrist_y and middle_tip_y < wrist_y and
                ring_tip_y < wrist_y and pinky_tip_y < wrist_y):
                if not backward:
                    pyautogui.keyDown("s")
                    backward = True
            else:
                if backward:
                    pyautogui.keyUp("s")
                    backward = False

            # Assign to respective hand
            if hand_side == "right":
                right_hand_open = is_hand_open
            else:
                left_hand_open = is_hand_open
                if right_hand_open and left_hand_open:
                    if not stop:
                        reset_controls()
                        stop = True
                    continue
                stop = False

    #Move Left (Leaning Left)
    if left_shoulder_y is not None and right_shoulder_y is not None:
        if left_shoulder_y > right_shoulder_y + 10:  # Tilt Left
            pyautogui.keyDown("a")
            moving_left = True
        else:
            if moving_left:
                pyautogui.keyUp("a")
                moving_left = False

    # Move Right (Leaning Right)
    if left_shoulder_y is not None and right_shoulder_y is not None:
        if right_shoulder_y > left_shoulder_y + 10:  # Tilt Right
            pyautogui.keyDown("d")
            moving_right = True
        else:
            if moving_right:
                pyautogui.keyUp("d")
                moving_right = False

    # SHOOT (Raise Right Elbow Above Shoulder)
    if right_elbow_y is not None and right_shoulder_y is not None:
        if right_elbow_y < right_shoulder_y:  # Elbow above shoulder
            if not shoot:
                pyautogui.keyDown("5")
                shoot = True
        else:
            if shoot:
                pyautogui.keyUp("5")
                shoot = False

    # RELOAD (Raise Left Elbow Above Shoulder)
    if left_elbow_y is not None and left_shoulder_y is not None:
        if left_elbow_y < left_shoulder_y:  # Elbow above shoulder
            if not reload:
                pyautogui.keyDown("r")
                reload = True
        else:
            if reload:
                pyautogui.keyUp("r")
                reload = False

    # SPIKE CONTROL (Left Hand Touching Right Elbow)
    if results_hands.multi_hand_landmarks:
        for handLms in results_hands.multi_hand_landmarks:
            landmarks = handLms.landmark

            left_index_x = landmarks[8].x * w  # Left Index Finger X
            left_index_y = landmarks[8].y * h  # Left Index Finger Y

            right_elbow_x = results_pose.pose_landmarks.landmark[14].x * w  # Right Elbow X
            right_elbow_y = results_pose.pose_landmarks.landmark[14].y * h  # Right Elbow Y

            # If left index finger is close to right elbow
            if abs(left_index_x - right_elbow_x) < 20 and abs(left_index_y - right_elbow_y) < 20:
                if not spike_controls:
                    pyautogui.keyDown("4")  # Example key for spike control
                    spike_controls = True
            else:
                if spike_controls:
                    pyautogui.keyUp("4")
                    spike_controls = False

    # Jump Condition (Both hands above head)
    if head_y is not None and right_wrist_y is not None and left_wrist_y is not None:
        if right_wrist_y < head_y and left_wrist_y < head_y:  # Hands above head → JUMP
            if not jump:
                pyautogui.keyDown("space")
                jump = True
        else:  # Stop jumping when hands lower
            if jump:
                pyautogui.keyUp("space")
                jump = False

    cv2.imshow("Image", img)
    cv2.waitKey(32)