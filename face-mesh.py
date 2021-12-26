import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec((0,255,0),2,1)

pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,mpDraw.DrawingSpec((0,255,0),0,0),mpDraw.DrawingSpec((0,255,0),1))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3 )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
