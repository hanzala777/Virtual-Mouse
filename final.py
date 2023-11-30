import cv2 as cv
import mediapipe as mp
import pyautogui
import time

cap = cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False
p_time = 0
middle_x = 0
middle_y = 0
index_y = 0
off_set_x = 0
off_set_y = 0
thumb_y = 0
index_5_y = 0
drag_offset_x = 0
drag_offset_y = 0
dragging = False

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img_height, img_width, _ = img.shape
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)

    multiLandMarks = result.multi_hand_landmarks

    if multiLandMarks:
        for handLMS in multiLandMarks:
            mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)
            last_x, last_y = pyautogui.position()
            landmarks = handLMS.landmark
            for hand_lms, landmark in enumerate(landmarks):
                x = int(landmark.x * img_width)
                y = int(landmark.y * img_height)
                if hand_lms == 12:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    middle_x = screen_width / img_width * x
                    middle_y = screen_height / img_height * y
                    # dif_x = middle_x - last_x
                    # dif_y = middle_y - last_y
                    # off_set_x = middle_x + dif_x
                    # off_set_y = middle_y + dif_y
                    # pyautogui.moveRel(off_set_x, off_set_y)
                if hand_lms == 8:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    index_x = screen_width / img_width * x
                    index_y = screen_height / img_height * y
                    if abs(middle_x - index_x) < 20:
                        print('left click: ', abs(middle_x - index_x))
                        pyautogui.leftClick()
                        time.sleep(1)
                    if abs(middle_x - index_x) > 75:
                        dif_x = middle_x - last_x
                        dif_y = middle_y - last_y
                        off_set_x = middle_x + dif_x
                        off_set_y = middle_y + dif_y
                        pyautogui.moveRel(off_set_x, off_set_y)
                if hand_lms == 4:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    thumb_x = screen_width / img_width * x
                    thumb_y = screen_height / img_height * y
                    # print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 70:
                        if not dragging:
                            pyautogui.mouseDown()
                            dragging = True
                            pyautogui.moveRel(drag_offset_x, drag_offset_y)
                    else:
                        if dragging:
                            pyautogui.mouseUp()
                            dragging = False
                if hand_lms == 5:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    index_5_x = screen_width / img_width * x
                    index_5_y = screen_height / img_height * y
                    # print(abs(index_y - index_5_y))
                    if abs(index_y - index_5_y) < 32:
                        pyautogui.scroll(-100)
                        time.sleep(0.5)
                if hand_lms == 16:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    ring_x = screen_width / img_width * x
                    ring_y = screen_height / img_height * y
                    # print(abs(ring_y - index_5_y))
                    if abs(ring_y - index_5_y) < 37:
                        pyautogui.scroll(100)
                        time.sleep(0.5)
                if hand_lms == 20:
                    cv.circle(img, (x, y), 20, (0, 0, 255))
                    little_x = screen_width / img_width * x
                    little_y = screen_height / img_height * y
                    if abs(little_y - index_5_y) < 35:
                        print('right click: ', abs(little_y - index_5_y))
                        pyautogui.rightClick()
                        time.sleep(1)
    if success:
        cv.imshow('Camera', img)
        if cv.waitKey(1) == ord('q'):
            pyautogui.mouseUp()  # Release mouse button before exiting
            break
    else:
        break

cap.release()
cv.destroyAllWindows()
