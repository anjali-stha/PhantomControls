import mediapipe as mp
import cv2
import pydirectinput

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
moving_left = False
moving_right = False
reload = False
spike_controls = False
stop = False

def reset_controls():
    pydirectinput.keyUp(5)
    pydirectinput.keyUp("space")
    pydirectinput.keyUp("w")
    pydirectinput.keyUp("s")
    pydirectinput.keyUp("a")
    pydirectinput.keyUp("d")
    pydirectinput.keyUp("r")
    pydirectinput.keyUp(4)

while True:
    success, img = cap.read()
    if not success:
        print("Camera not found!")
        break

    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_pose = Pose.process(imgrgb)
    results_hands = hands.process(imgrgb)

    right_wrist_y = None
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
        h, w, c = img.shape 

        for id, lm in enumerate(results_pose.pose_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)

            if id == 16:  
                right_wrist_y = cy
            elif id == 15:  
                left_wrist_y = cy
            elif id == 0: 
                head_y = cy
            elif id == 11: 
                left_shoulder_y = cy
            elif id == 12:  
                right_shoulder_y = cy
            if id == 14: 
                right_elbow_y = cy
            elif id == 13:
                left_elbow_y = cy

            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    
    if results_hands.multi_hand_landmarks:
        for handLms in results_hands.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            h, w, c = img.shape
            landmarks = handLms.landmark

            wrist_y = landmarks[0].y * h
            index_tip_y = landmarks[8].y * h
            thumb_tip_y = landmarks[4].y * h
            middle_tip_y = landmarks[12].y * h
            ring_tip_y = landmarks[16].y * h
            pinky_tip_y = landmarks[20].y * h

            hand_side = "right" if landmarks[0].x > 0.5 else "left"

            is_hand_open = (
                index_tip_y < wrist_y and middle_tip_y < wrist_y and
                ring_tip_y < wrist_y and pinky_tip_y < wrist_y
            )

            if thumb_tip_y < wrist_y and index_tip_y < wrist_y and is_hand_open:
                if not forward:
                    pydirectinput.keyDown("w")
                    forward = True
            else:
                if forward:
                    pydirectinput.keyUp("w")
                    forward = False

            if thumb_tip_y > wrist_y and index_tip_y > wrist_y:
                if not backward:
                    pydirectinput.keyDown("s")
                    backward = True
            else:
                if backward:
                    pydirectinput.keyUp("s")
                    backward = False

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

            thumb_tip_x = landmarks[4].x * w  
            thumb_tip_y = landmarks[4].y * h 
            index_tip_x = landmarks[8].x * w  
            index_tip_y = landmarks[8].y * h  

            if abs(thumb_tip_x - index_tip_x) < 20 and abs(thumb_tip_y - index_tip_y) < 20:
                if not shoot:
                    pydirectinput.keyDown("5")  
            else:
                if shoot:
                    pydirectinput.keyUp("5")
                    shoot = False

    
    if left_shoulder_y is not None and right_shoulder_y is not None:
        if left_shoulder_y > right_shoulder_y + 10:  # Tilt Left
            pydirectinput.keyDown("a")
            moving_left = True
        else:
            if moving_left:
                pydirectinput.keyUp("a")
                moving_left = False

    
    if left_shoulder_y is not None and right_shoulder_y is not None:
        if right_shoulder_y > left_shoulder_y + 10:  # Tilt Right
            pydirectinput.keyDown("d")
            moving_right = True
        else:
            if moving_right:
                pydirectinput.keyUp("d")
                moving_right = False

    
    if left_elbow_y is not None and left_shoulder_y is not None:
        if left_elbow_y < left_shoulder_y:  # Elbow above shoulder
            if not reload:
                pydirectinput.keyDown("r")
                reload = True
        else:
            if reload:
                pydirectinput.keyUp("r")
                reload = False

    if results_hands.multi_hand_landmarks:
        for handLms in results_hands.multi_hand_landmarks:
            landmarks = handLms.landmark

            left_index_x = landmarks[8].x * w  
            left_index_y = landmarks[8].y * h  

            right_elbow_x = results_pose.pose_landmarks.landmark[14].x * w  
            right_elbow_y = results_pose.pose_landmarks.landmark[14].y * h  
            
            if abs(left_index_x - right_elbow_x) < 20 and abs(left_index_y - right_elbow_y) < 20:
                if not spike_controls:
                    pydirectinput.keyDown("4")  
                    spike_controls = True
            else:
                if spike_controls:
                    pydirectinput.keyUp("4")
                    spike_controls = False

    if head_y is not None and right_wrist_y is not None and left_wrist_y is not None:
        if right_wrist_y < head_y and left_wrist_y < head_y:  
            if not jump:
                pydirectinput.keyDown("space")
                jump = True
        else:  
            if jump:
                pydirectinput.keyUp("space")
                jump = False

    cv2.imshow("Image", img)
    cv2.waitKey(32)
