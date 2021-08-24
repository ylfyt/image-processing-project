from classes.camera import Camera
from classes.mask import Mask
from classes.config import Config
import cv2

def getPicture(frame):
    cv2.imwrite('img/out.jpg', frame)
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

cam = Camera(ipCam=True, width=480, height=320)
colorMasks = Config.getColorMasks()

while True:
    # frame = cam.getVideo()

    frame = cv2.imread("img/out2.jpg")

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    for mask in colorMasks:
        mask.updateFrame(frame=hsv_frame)

    # n = cv2.countNonZero(blueMask.getMask())
    # print(n)

    # for mask in colorMasks:
    #     mask.drawContours(frame=frame)

    colorMasks[2].drawContours(frame)

    # m = cv2.mean(frame, blueMask.getMask())
    # wl = getWaveLength(m[2], m[1], m[0])

    # print(m)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    # Press Esc key to exit
    if (key == 27):
        break
    if(key == 32):
        getPicture(frame)
  
cv2.destroyAllWindows()
