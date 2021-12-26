import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            if id == 2:
                cv2.circle(img, (cx, cy), 15, (56, 217, 28), cv2.FILLED)
            if id == 5:
                cv2.circle(img, (cx, cy), 15, (56, 217, 28), cv2.FILLED)

        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_ITALIC, 1, (128, 64, 45), 3 )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
