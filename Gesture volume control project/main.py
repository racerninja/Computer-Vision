import cv2
import numpy as np
import time
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.9) #high confidence mode
mpDraw = mp.solutions.drawing_utils

L_MIN = 25
L_MAX = 250

cap.set(3,720)
cap.set(4,480)

pTime = 0

#audio config
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

vol_bar = 397
vol_percent = 0

vol_range = volume.GetVolumeRange()
VOL_MIN = vol_range[0]
VOL_MAX = vol_range[1]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    cv2.circle(img,(cx,cy),15,(56, 217, 28), cv2.FILLED)
                    x1,y1 = cx,cy
                if id == 8:
                    cv2.circle(img,(cx,cy),15,(56, 217, 28), cv2.FILLED)
                    x2,y2 = cx,cy

            cv2.line(img,(x1,y1),(x2,y2),(56,217,28),3)
            x0,y0 = (x1+x2)//2, (y1+y2)//2
            cv2.circle(img, (x0, y0), 15, (56, 217, 28), cv2.FILLED)
            length = math.hypot((x2-x1),(y2-y1))

            if length<50:
                cv2.circle(img, (x0, y0), 15, (0,0,255), cv2.FILLED)
            vol = np.interp(length, [25, 250], [VOL_MIN, VOL_MAX])

            vol_bar = np.interp(length, [25, 250], [397,156])
            vol_percent = np.interp(length, [25,250], [0,100])

            volume.SetMasterVolumeLevel(vol, None)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.rectangle(img, (50,150), (75,400), (0,0,0), 3)
    cv2.rectangle(img, (53,int(vol_bar)-3), (72,400-3), (0,0,255), cv2.FILLED)
    cv2.putText(img, str(int(vol_percent)) + "%", (35,450), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2 )

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3 )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
