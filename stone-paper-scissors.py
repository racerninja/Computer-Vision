import cv2
import mediapipe as mp
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#PLAY WITH RIGHT HAND

RESULT = ""
PREV_RESULT = ""
SPS = ["STONE", "PAPER", "SCISSORS"]
PLAYER_SCORE = 0
ROUND = 1
COMP_SCORE = 0
pTime = 0
sps = None

def posy(id):
    return int(lm.y*h)

def posx(id):
    return int(lm.x*w)

def choose(SPS):
    r = random.randint(0,2)
    return SPS[r]

while True:

    ROUND = max(ROUND, PLAYER_SCORE + COMP_SCORE + 1)
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

                if id==8 or id== 12 or id == 16 or id == 20:
                    cv2.circle(img,(posx(id),posy(id)),10,(56, 217, 28), cv2.FILLED)

            if len(list) != 0:

                T1, T2, T3, T4, T5, T6 = 0, 0, 0, 0, 0, 0

                V1 = [0,1,2,3,4,13,14,15,16,17,18,19,20]
                V2 = [0,1,2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]

                #scissors

                for i in V1:
                    if list[i][2] > list[8][2] and list[i][2] > list[12][2]:
                        T1 += 1
                    if list[i][1] < list[8][1] and list[i][1] < list[12][1]:
                        T2 += 1

                dis1 = abs(list[8][1] - list[12][1])
                dis2 = abs(list[5][1] - list[9][1])

                if (T1 == 13 or T2 == 13) and dis1 > 2*dis2:
                    RESULT = "SCISSORS"

                    if PREV_RESULT == "REFRESH":
                        sps = choose(SPS)

                #paper

                if list[8][2]<list[5][2]:
                    T3+=1
                if list[12][2]<list[9][2]:
                    T3+=1
                if list[16][2]<list[13][2]:
                    T3+=1
                if list[20][2]<list[17][2]:
                    T3+=1

                if T3 == 4:
                    RESULT = "PAPER"

                    if PREV_RESULT == "REFRESH":
                        sps = choose(SPS)

                #stone

                for i in V2:
                    if list[i][2] > list[5][2] and list[i][2] > list[9][2] and list[i][2] > list[13][2] and list[i][2] > list[17][2]:
                        T4+=1
                if T4 == 17:
                    RESULT = "STONE"

                    if PREV_RESULT == "REFRESH":
                        sps = choose(SPS)

                # refresh

                if list[8][2]>list[6][2]:
                    T6+=1
                if list[12][2]>list[10][2]:
                    T6+=1
                if list[16][2]>list[14][2]:
                    T6+=1
                if list[20][2]>list[18][2]:
                    T6+=1

                if T6 == 4:
                    RESULT = "REFRESH"
                    sps = None

                PREV_RESULT = RESULT
                cv2.putText(img, str(RESULT), (470, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
                cv2.putText(img, sps, (30, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.putText(img, "ROUND: " + str(ROUND), (30, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(img, "PLAYER SCORE: " + str(PLAYER_SCORE), (400, 420), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
    cv2.putText(img, "COMP SCORE: " + str(COMP_SCORE), (400, 450), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

    if sps == RESULT and sps != "":
        sps = None
        ROUND += 1
        RESULT = "REFRESH"
        cv2.rectangle(img, (450,300,150,50), (0,0,0), -1)
        cv2.putText(img, "DRAW", (470, 340), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    if (sps == "STONE" and RESULT == "PAPER") or (sps == "PAPER" and RESULT == "SCISSORS") or (sps == "SCISSORS" and RESULT == "STONE"):
        PLAYER_SCORE +=1
        sps = None
        RESULT = "REFRESH"
        cv2.rectangle(img, (450, 300, 150, 50), (0, 0, 0), -1)
        cv2.putText(img, "WON", (470, 340), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    if (sps == "PAPER" and RESULT == "STONE") or (sps == "SCISSORS" and RESULT == "PAPER") or (sps == "STONE" and RESULT == "SCISSORS"):
        COMP_SCORE +=1
        sps = None
        RESULT = "REFRESH"
        cv2.rectangle(img, (450, 300, 150, 50), (0, 0, 0), -1)
        cv2.putText(img, "LOST", (470, 340), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3 )

    cv2.imshow("Image", img)
    cv2.waitKey(1)
