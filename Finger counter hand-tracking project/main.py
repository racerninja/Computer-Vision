import cv2
import mediapipe as mp
import time
import os

cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
COUNT = 0
HAND = ""

def posy(id):
    return int(lm.y*h)

def posx(id):
    return int(lm.x*w)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            list = []
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cy = int(lm.y * h)
                cx = int(lm.x * w)
                list.append([id,cx,cy])

                if id==4 or id==8 or id==12 or id==16 or id==20:
                    cv2.circle(img,(posx(id),posy(id)),10,(56, 217, 28), cv2.FILLED)

            if len(list)!=0:
                COUNT = 0
                if list[4][1]<list[20][1]:
                    HAND = "LEFT"
                    cv2.putText(img, HAND, (490, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

                if list[4][1]>list[20][1]:
                    HAND = "RIGHT"
                    cv2.putText(img, HAND, (480, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

                if list[4][1]>list[2][1] and HAND == "RIGHT":
                    COUNT+=1
                if list[4][1]<list[2][1] and HAND == "LEFT":
                    COUNT+=1

                if list[8][2]<list[6][2]:
                    COUNT+=1
                if list[12][2]<list[10][2]:
                    COUNT+=1
                if list[16][2]<list[14][2]:
                    COUNT+=1
                if list[20][2]<list[18][2]:
                    COUNT+=1

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3 )
    cv2.putText(img, str(COUNT), (530, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
