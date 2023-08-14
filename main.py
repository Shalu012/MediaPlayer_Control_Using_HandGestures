import cv2 
import mediapipe as mp
import pyautogui
import time

def count_fingers(hnd):
    count = 0

    thresh_value = (hnd.landmark[0].y*100 - hnd.landmark[9].y*100)/2

    if (hnd.landmark[5].y*100 - hnd.landmark[8].y*100) > thresh_value:
        count += 1

    if (hnd.landmark[9].y*100 - hnd.landmark[12].y*100) > thresh_value:
        count += 1

    if (hnd.landmark[13].y*100 - hnd.landmark[16].y*100) > thresh_value:
        count += 1

    if (hnd.landmark[17].y*100 - hnd.landmark[20].y*100) > thresh_value:
        count += 1

    if (hnd.landmark[5].x*100 - hnd.landmark[4].x*100) > 6:
        count += 1


    return count 

capture = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)


start = False 

prev = -1

while True:
    end_time = time.time()
    _, frame = capture.read()
    frame = cv2.flip(frame, 1)

    res = hand_obj.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:

        hand_keyPoints = res.multi_hand_landmarks[0]

        count = count_fingers(hand_keyPoints)

        if not(prev==count):
            if not(start):
                start_time = time.time()
                start = True

            elif (end_time-start_time) > 0.2:
                if (count == 1):
                    pyautogui.press("right")
                
                elif (count == 2):
                    pyautogui.press("left")

                elif (count == 3):
                    pyautogui.press("up")

                elif (count == 4):
                    pyautogui.press("down")

                elif (count == 5):
                    pyautogui.press("space")

                prev = count
                start = False


        


        drawing.draw_landmarks(frame, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("Img", frame)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break