import requests
import cv2
import numpy as np
import imutils
  
class Mask:
    def __init__(self, name, frame,low, high):
        self.SIZEOFMINCONTOURAREA = 1000
        self.THICKNESSOFCONTOUREDGE = 1

        self.name = name
        self.lower = np.array(low)
        self.upper = np.array(high)
        self.mask = cv2.inRange(src=frame, lowerb=self.lower, upperb=self.upper)
    
    def getMask(self):
        return self.mask

    def getContours(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours

    def drawContours(self, frame):
        for c in self.getContours():
            area = cv2.contourArea(c)
            if (area > self.SIZEOFMINCONTOURAREA):
                cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=self.THICKNESSOFCONTOUREDGE)

                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)
                cv2.putText(frame, self.name, (cx-0, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)


class Camera:
    def __init__(self, ipCam, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.fromIpCam = ipCam
        self.cap = 1
        self.url = "http://192.168.43.37:8080/shot.jpg"

        if (not self.fromIpCam):
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)


    def getVideo(self):
        frame = 1
        if (self.fromIpCam):
            img_resp = requests.get(self.url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            frame = imutils.resize(img, width=self.WIDTH, height=self.HEIGHT)
        else:
            _, frame = self.cap.read()

        return frame

cam = Camera(ipCam=True, width=480, height=320)

  
# While loop to continuously fetching data from the Url
while True:
    frame = cam.getVideo()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    redMask = Mask(name="RED", frame=hsv_frame, low=[0, 85, 65], high=[10, 255, 255])

    redMask2 = Mask(name="RED", frame=hsv_frame, low=[160, 85, 65], high=[179, 255, 255])

    blueMask = Mask(name="BLUE", frame=hsv_frame, low=[95, 100, 70], high=[130, 255, 255])

    greenMask = Mask(name="GREEN", frame=hsv_frame, low=[35, 95, 70], high=[80, 255, 255])

    orangeMask = Mask(name="ORANGE", frame=hsv_frame, low=[10, 100, 20], high=[10, 100, 20])

    exceptWhiteMask = Mask(name="WHITE", frame=hsv_frame, low=[0, 42, 0], high=[179, 255, 255])

    redMask.drawContours(frame=frame)
    redMask2.drawContours(frame)
    blueMask.drawContours(frame)
    greenMask.drawContours(frame)

    cv2.imshow("Android_cam", frame)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()
