from numpy import info
from classes.camera import Camera
from classes.scan_state import ScanState
from classes.mask import Mask
from classes.config import Config
import cv2
import time

from classes.scan_state import ScanState



def getPicture(frame):
    cv2.imwrite('../img/out.jpg', frame)
    print("Success")

def getWaveLength(r, g, b):
    red = int(r)
    green = int(g)
    blue = int(b)
    return red * green * blue

def getCondition(wavelength):
    aaa = 0
    if (aaa == 1):
        return "Parah"
    elif (aaa == 2):
        return "Tidak parah"
    else:
        return "Santuy"

def getMaxMask(masks):
    idxMax = 0
    for i in range(len(masks)):
        nMax = cv2.countNonZero(masks[idxMax].getMask())
        n = cv2.countNonZero(masks[i].getMask())
        if (n > nMax):
            idxMax = i
    
    return [masks[idxMax], cv2.countNonZero(masks[idxMax].getMask())]

cam = Camera(ipCam=True, width=480, height=320)
colorMasks = Config.getColorMasks()

while True:
    # frame = cam.getVideo()

    frame = cv2.imread("../img/1.jpg")

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for mask in colorMasks:
        mask.updateFrame(frame=hsv_frame)

    info = getMaxMask(colorMasks)
    maxMask = info[0]
    nMax = info[1]

    if (nMax > 750):

        meanRGB = cv2.mean(frame, maxMask.getMask())
        wavelength = getWaveLength(meanRGB[2], meanRGB[1], meanRGB[0])
        condition = getCondition(wavelength)

        maxMask.drawContours(frame, condition)
    
    if (ScanState.isResetState()):
        ScanState.setScanningState()

    print(ScanState.getState())

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    # Press Esc key to exit
    if (key == 27):
        break
    if(key == 32):
        getPicture(frame)
    if (key == 115):
        ScanState.setResetState()
  
cv2.destroyAllWindows()
