import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########## Basic Camera Setting
weightCam, heightCam = 900, 600
##########

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, weightCam)  # Set camera width
cap.set(4, heightCam)  # Set camera height
pTime = 0 # Previous time (for FPS calculation)

# Initialize hand detector with 0.7 detection confidence
detector = htm.HandDetector(detectionCon=0.7)

# Initialize audio interface using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = interface.QueryInterface(IAudioEndpointVolume)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

# Get the volume range of the system
volRange = volume.GetVolumeRange()
# print(volume.GetVolumeRange())
minVol = volRange[0] # Minimum volume (usually around -65 dB)
maxVol = volRange[1] # Maximum volume (usually 0 dB)
vol = 0 # Current volume level
volBar = 400 # Y-coordinate for volume bar display
volPer = 0  # Current volume percentage

while True:  # Read frame from webcam
    success, img = cap.read()
    img = detector.findHands(img)  # Detect hands and landmarks in the frame
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8]) #For thumb and index finger, getting coordinatesF
        x1, y1 = lmList[4][1], lmList[4][2] #First element as x and second element as y
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        #Draw circle on thumb and index point
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED) #Center circle

        length = math.hypot(x2-x1, y2-y1) # Calculate distance between thumb and index finger
        #print(length)

        #Hand range lies between 8 - 200, And our volume range is -65 - 0.
        vol = np.interp(length,[8, 200], [minVol, maxVol]) #Interpolate between minVol and maxVol based
        volBar = np.interp(length,[8, 200], [400, 150])
        volPer = np.interp(length,[8, 200], [0, 100])
        print(int(length), vol) # Print length and volume (for debugging/logging)
        volume.SetMasterVolumeLevel(vol, None)# Set the system master volume level

        if length <30: # If fingers are very close, change center circle color to green
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED) 

    # Draw volume bar background and fill
    cv2.rectangle(img,(50, 150), (85,400), (255, 0, 0), 3)
    cv2.rectangle(img,(50, int(volBar)), (85,400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f"Volume:{int(volPer)} %", (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3) #For volume percentage

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS:{int(fps)}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3) #FPS Count 

    cv2.imshow("Img", img) # Show the processed frame
    cv2.waitKey(1)

    