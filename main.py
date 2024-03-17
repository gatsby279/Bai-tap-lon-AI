import cv2 as cv
import HandTrackingModule as htm
import pyautogui
import numpy as np

"""
năm tay và chỉ dơ ngón trỏ để điều khiển chuột , do cái cam của tôi để nên tôi để smooth = 4, 
anh em có cam xin thì chỉnh smooth lền cao hơn để nó nhậy hơn nhá
còn để click : dơ cả ngon dữa và ngón trỏ và khẽ chạm để click
"""


# start cam
success = False
while success == False:
    cap = cv.VideoCapture(0)
    success, _ = cap.read()
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# frame screen
screenControl = 100

# làm mượt
smoothening = 4

#
detector = htm.handDetector()

# kích thước màn hình
wScr, hScr = pyautogui.size()
print(wScr, hScr)

# vị trí
newLocX, newLocY = wScr / 2, hScr / 2
oldLocX, oldLocY = wScr / 2, hScr / 2

while True:
    # 1. tìm vị trí tay và giá trị khác
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. xứ lý khi phát hiện tay
    if len(lmList) != 0:
        cv.rectangle(img, (screenControl, screenControl), (wCam - screenControl, hCam - screenControl), (255, 255, 255), 2)

        # lấy ra thông tin ngón tay
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. danh sách trạng thát của các ngón : nắm hay duỗi
        fingers = detector.fingersUp()

        # 4. chế độ điều khiển : ngón trỏ duỗi, ngón giữa nắm
        if fingers[1] == 1 and fingers[2] == 0:

            # 5. chuyển đổi giá trị vị trí chuột tương ứng với vị trí ngón trỏ
            mouse_x = np.interp(x1, (screenControl, wCam - screenControl), (0, wScr))
            mouse_y = np.interp(y1, (screenControl, hCam - screenControl), (0, hScr))

            # 6. làm mượt gia trị
            newLocX = oldLocX + (mouse_x - oldLocX) / smoothening
            newLocY = oldLocY + (mouse_y - oldLocY) / smoothening

            # 7. di chuyển chuột
            pyautogui.moveTo(newLocX, newLocY)
            cv.circle(img, (x1, y1), 10, (0, 0 , 255), cv.FILLED)
            oldLocX, oldLocY = newLocX, newLocY

        # 8. nếu cả ngón trỏ và ngón giữa cùng duỗi : dữ nguyên chuột
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. tìm khoảng cách giữa 2 ngón
            distance, img, infoLine = detector.findDistance(8, 12, img)
            print(distance)
            if distance < 30:
                # click chuột
                pyautogui.click()
                cv.circle(img, (infoLine[4], infoLine[5]), 10, (0, 255, 0), cv.FILLED)

    cv.imshow("powered by Kien Huy", img)
    cv.waitKey(1)
