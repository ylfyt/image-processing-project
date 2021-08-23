import cv2
import numpy as np
import imutils

class Mask:
    def __init__(self, name, low, high):
        self.SIZEOFMINCONTOURAREA = 1000
        self.THICKNESSOFCONTOUREDGE = 2

        self.name = name
        self.lower = np.array(low)
        self.upper = np.array(high)
    
    def getMask(self):
        return self.mask

    def updateFrame(self, frame):
        self.mask = cv2.inRange(src=frame, lowerb=self.lower, upperb=self.upper)

    def getContours(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours

    def drawContours(self, frame):
        con = self.getContours()

        areas = [cv2.contourArea(c) for c in con]
        idxMax = 0
        for i in range(1, len(areas)):
            if (areas[idxMax] < areas[i]):
                idxMax = i


        for idx, c in enumerate(con):
            area = cv2.contourArea(c)
            if (area > self.SIZEOFMINCONTOURAREA):
                cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=self.THICKNESSOFCONTOUREDGE)

                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)
                cv2.putText(frame, self.name, (cx-0, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)