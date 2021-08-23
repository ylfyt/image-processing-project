import requests
import cv2
import numpy as np
import imutils
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.


class Mask:
    def __init__(self, frame,low, high):
        self.lower = np.array(low)
        self.upper = np.array(high)
        self.mask = cv2.inRange(src=frame, lowerb=self.lower, upperb=self.upper)
    
    def getMask(self):
        return self.mask

    def getContours(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours



WIDTH = 480
HEIGHT = 320

fromIpCam = True
cap = 1
url = "http://192.168.43.37:8080/shot.jpg"


SIZEOFMINCONTOURAREA = 500
THICKNESSOFCONTOUREDGE = 1


if (not fromIpCam):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


def getVideoFromIPCam():
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    frame = imutils.resize(img, width=WIDTH, height=HEIGHT)

    return frame

def getVideoFromCamera():
    _, frame = cap.read()

    return frame


  
# While loop to continuously fetching data from the Url
while True:
    frame = 1
    if (fromIpCam):
        frame = getVideoFromIPCam()
    else:
        frame = getVideoFromCamera()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color
    # red = cv2.bitwise_and(frame, frame, mask=red_mask)
    redMask = Mask(frame=hsv_frame, low=[0, 85, 65], high=[10, 255, 255])

    # Red color 2
    redMask2 = Mask(frame=hsv_frame, low=[160, 85, 65], high=[179, 255, 255])

    # Blue color
    blueMask = Mask(frame=hsv_frame, low=[95, 100, 70], high=[130, 255, 255])

    # Green color
    greenMask = Mask(frame=hsv_frame, low=[35, 95, 70], high=[80, 255, 255])

    # orange color
    orangeMask = Mask(frame=hsv_frame, low=[10, 100, 20], high=[10, 100, 20])

    # Every color except white
    exceptWhiteMask = Mask(frame=hsv_frame, low=[0, 42, 0], high=[179, 255, 255])
    
  

    redContours = redMask.getContours()

    redContours2 = redMask2.getContours()

    blueContours = blueMask.getContours()

    greenContours = greenMask.getContours()


    for c in blueContours:
        area = cv2.contourArea(c)
        if (area > SIZEOFMINCONTOURAREA):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=THICKNESSOFCONTOUREDGE)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Blue", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    for c in redContours:
        area = cv2.contourArea(c)
        if (area > SIZEOFMINCONTOURAREA):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=THICKNESSOFCONTOUREDGE)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Red", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    for c in redContours2:
        area = cv2.contourArea(c)
        if (area > SIZEOFMINCONTOURAREA):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=THICKNESSOFCONTOUREDGE)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Red", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    
    for c in greenContours:
        area = cv2.contourArea(c)
        if (area > SIZEOFMINCONTOURAREA):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=THICKNESSOFCONTOUREDGE)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Green", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)


    cv2.imshow("Android_cam", frame)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()
