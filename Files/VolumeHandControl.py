import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


########## Camera Setting
weightCam, heightCam = 900, 600
##########

cap = cv2.VideoCapture(0)
cap.set(3, weightCam)
cap.set(4, heightCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = interface.QueryInterface(IAudioEndpointVolume)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# print(volume.GetVolumeRange())
minVol = volRange[0]
maxVol = volRange[1]


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        #print(lmList[4], lmList[8]) #For thumb and index finger

        x1, y1 = lmList[4][1], lmList[4][2] #First element as x and second element as y
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        #Draw circle on thumb and index point
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED) #Center circle

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        #Hand range lies between 8 - 200, And our volume range is -65 - 0.
        vol = np.interp(length,[8, 200], [minVol, maxVol]) #Interpolate between minVol and maxVol based
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length <30:
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED) 



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS:{int(fps)}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

    