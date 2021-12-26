import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpFace = mp.solutions.face_detection
face = mpFace.FaceDetection()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            h, w, c = img.shape
            target_square = detection.location_data.relative_bounding_box
            square = int(target_square.xmin*w), int(target_square.ymin*h),int(target_square.width*w), int(target_square.height*h)
            cv2.rectangle(img, square, (0,255,0), 2)
            cv2.putText(img, str(int(detection.score[0]*100)) + "%", (square[0], square[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3 )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
