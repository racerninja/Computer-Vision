import cv2
import math

path = "C:\\Users\\user\\Desktop\\pixels\\mac.jpg" #absolute file path
img = cv2.imread(path)
img = cv2.resize(img, (720,480)) #resize

point_list = [] #list of pt. vectors

def draw(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        l = len(point_list)
        if l != 0 and l%3 != 0: #breaks path after 2 lines
            cv2.line(img, point_list[l-1], (x,y), (0,0,255), 2) #joins curr pt with prev pt

        cv2.circle(img, (x,y), 5, (0,0,255),cv2.FILLED ) #pt highlighted with cv tool
        point_list.append([x,y])

def grad(pt1, pt2):
    if pt1[0]-pt2[0] != 0: #calculation of relative gradient
        return (pt1[1]-pt2[1])/(pt1[0]-pt2[0])
    else:
        return math.inf #infinity case

def get_angle(point_list):
    x, y, z = point_list[l-3], point_list[l-2], point_list[l-1]
    m1 = grad(y,x)
    m2 = grad(y,z)

    if m1 == math.inf == m2:
        angle = 180 #st. line

    elif m1*m2 == -1:
        angle = 90 #tangent inverse infinity case

    elif m1 == math.inf:
        m1 = 0 #wrt 0 gradient axis
        angle = get_abs_angle(point_list, m1, m2) #absolute angle
        angle += 90 #correction
        cv2.putText(img, str(angle), (y[0] - 40, y[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    elif m2 == math.inf:
        m2 = 0 #wrt 0 gradient axis
        angle = get_abs_angle(point_list, m1, m2) #absolute angle
        angle += 90 #correction
        cv2.putText(img, str(angle), (y[0] - 40, y[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    else:
        angle = get_abs_angle(point_list, m1, m2) 
        cv2.putText(img, str(angle), (y[0] - 40, y[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2) #display text

def get_abs_angle(point_list, m1, m2): #calculation of absolute angle
    x, y, z = point_list[l-3], point_list[l-2], point_list[l-1]

    if y[0] < x[0] and y[0] < z[0]: 
        #calculation with tangent inverse
        angle = (round(math.degrees(math.atan(abs(m1 - m2) / (1 + m1 * m2))))) #acute
        if angle < 0:
            angle = 180 - abs(angle) #obtuse

    elif x[0] < y[0] and y[0] < z[0]:
        angle = 180 - (round(math.degrees(math.atan(abs(m1 - m2) / (1 + m1 * m2))))) #only obtuse possible

    elif x[0] > y[0] and y[0] > z[0]:
        angle = 180 - (round(math.degrees(math.atan(abs(m1 - m2) / (1 + m1 * m2))))) #only obtuse possible

    elif y[0] > x[0] and y[0] > z[0]:
        angle = (round(math.degrees(math.atan(abs(m1 - m2) / (1 + m1 * m2))))) #acute
        if angle < 0:
            angle = 180 - abs(angle) #obtuse

    else:
        #case of infinite slop
        angle = (round(math.degrees(math.atan(abs(m1 - m2) / (1 + m1 * m2)))))
    return angle

while True:
    cv2.imshow("Angle Finder", img)
    cv2.setMouseCallback("Angle Finder", draw)
    if cv2.waitKey(1) & 0xFF == ord(" "): #masking with 1111 1111 to restart loop when 32 (SPACE is pressed) while new layer masks the old one on window
        point_list = [] #array re-assigned
        img = cv2.imread(path)
        img = cv2.resize(img, (720, 480)) #resized for new layer

    l = len(point_list)
    if l%3 == 0 and l != 0:
        get_angle(point_list) #gets angle after every 3 points
