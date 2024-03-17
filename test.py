import cv2 as cv
import mediapipe as mp
import pyautogui
import math

# webcam
cam = cv.VideoCapture(0)
success, _ = cam.read()
while success == False:
    cam = cv.VideoCapture(0)
    success, _ = cam.read()

# object hands
module_hands = mp.solutions.hands
object_hands = module_hands.Hands()

# drawing utils
drawing_utils = mp.solutions.drawing_utils

# Tắt tính năng bảo vệ fail-safe
pyautogui.FAILSAFE = False

while True:

    success, img = cam.read()
    img = cv.flip(img, 1)

    img_RGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)    # chuyển đổi hệ màu sắc cho máy tính xử lý
    process = object_hands.process(img_RGB)     # nhập thông tin dữ liệu hình ảnh cho object_hands
    hand_landmarks = process.multi_hand_landmarks    # danh sách các bàn tay xuất hiện trong frame và thuộc tính kém theo

    if hand_landmarks:
        # parameter for showing
        frame_h, frame_w, _ = img.shape
        screen_w, screen_h = pyautogui.size()
        print(screen_w, screen_h, "-", frame_w, frame_h)

        for hand_landmark in hand_landmarks:
            # draw all points
            drawing_utils.draw_landmarks(img, hand_landmark, module_hands.HAND_CONNECTIONS)

            # draw small screen
            start_x, start_y = int(frame_w/2 - screen_w/8), int(frame_h/2 - screen_h/8)
            end_x, end_y = int(frame_w/2 + screen_w/8), int(frame_h/2 + screen_h/8)
            cv.rectangle(img, (start_x, start_y), (end_x, end_y), (255,255,255), 1)

            # draw hand mouse
            mouse = hand_landmark.landmark[8]
            mouse_x, mouse_y = int(mouse.x * frame_w), int(mouse.y * frame_h)
            cv.circle(img, (mouse_x, mouse_y), 6, (0, 0, 255), cv.FILLED)

            # move mouse
            position_x = mouse_x - start_x
            if position_x <= 0: position_x = 0
            elif position_x >= end_x: position_x = end_x
            position_y = mouse_y - start_y
            if position_y <= 0: position_y = 0
            elif position_y >= end_y: position_y = end_y
            pyautogui.moveTo(position_x * 4, position_y * 4)  # move mouse

            # draw control point
            control = hand_landmark.landmark[4]
            control_x, control_y = int(control.x * frame_w), int(control.y * frame_h)
            cv.circle(img, (control_x, control_y), 6, (128, 0, 0), cv.FILLED)

            # draw click point and control
            click = hand_landmark.landmark[12]
            click_x, click_y = int(click.x * frame_w), int(click.y * frame_h)
            cv.circle(img, (click_x, click_y), 6, (128, 0, 0), cv.FILLED)
            distance_click = math.sqrt(math.pow(control_x - click_x, 2) + math.pow(control_y - click_y, 2))
            if int(distance_click) < 25:
                pyautogui.click()


            keyboard = hand_landmark.landmark[20]
            keyboard_x, keyboard_y = int(keyboard.x * frame_w), int(keyboard.y * frame_h)
            cv.circle(img, (keyboard_x, keyboard_y), 5, (128, 0, 0), cv.FILLED)

    cv.imshow("image", img)
    cv.waitKey(1)