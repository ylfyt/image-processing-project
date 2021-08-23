import requests
import cv2
import imutils
import numpy as np

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
    
    def getPicture(self, frame):
        cv2.imwrite('img/out.jpg',frame)
        print("Success")