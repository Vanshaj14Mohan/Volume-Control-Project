import cv2
import time
import numpy as np
import HandTrackingModule as htm


########## Camera setting
weightCam, heightCam = 900, 600
##########

cap = cv2.VideoCapture(0)
cap.set(3, weightCam)
cap.set(4, heightCam)
pTime = 0

detector = htm.HandDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS:{int(fps)}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)