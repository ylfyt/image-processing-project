from time import sleep
import datetime
from threading import *
# import RPi.GPIO as GPIO
from gpiozero import Button
import cv2
from classes.scan_state import ScanState

# from gpiozero import Button
# from time import sleep

# button = Button(6)

# while True:
#     if button.is_pressed:
#         print("Button is pressed")
#     else:
#         print("Button is not pressed")

#     sleep(1)

# from gpiozero import LED
# from time import sleep

# led = LED(24)

# while True:
#     led.on()
#     sleep(1)
#     led.off()
#     sleep(1)


# GPIO.setmode(GPIO.BOARD)
btnFlash=Button(16)     # flash
btnFlashPressed = False
btnPhoto=20      # take photo
btnReset= Button(21)
LED=12           # LED
BUZZER=18        # Buzzer
# GPIO.setup(btnFlash,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnPhoto,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnReset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED,GPIO.OUT)
# GPIO.setup(BUZZER,GPIO.OUT)
flagLED=False
flagBuzzer=False


# class state

def signal(indicator, flagSignal, repeat):
    for i in range(repeat):
        if flagSignal==False:
            GPIO.output(indicator,True)
            flagSignal=True
            sleep(0.5)
        else:
            GPIO.output(indicator, False)
            flagSignal=False
            sleep(0.5)

def getPicture(frame, cond):
    path = '../img/' + '{%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '_' + cond + '.jpg'
    cv2.imwrite(path, frame)
    print("Scanned")
    return path

def controlBtn(frame):
    if btnFlash.is_pressed and not ScanState.btnFlashPressed:
        print("btnFlash Was Pressed:")
        Thread( target=signal(LED, flagLED, 1) ).start()
        Thread( target=signal(BUZZER, flagBuzzer, 1) ).start()
    ScanState.btnFlashPressed = btnFlash.is_pressed
        
    if btnReset.is_pressed and not ScanState.btnResetPressed:
        print("btnReset Was Pressed:")
        # clear class state
        Thread( target=signal(BUZZER, flagBuzzer, 1) ).start()
        if (ScanState.isState("picture")):
            ScanState.setIdleState()
        elif (ScanState.isState("idle")):
            ScanState.resetScan()
    ScanState.btnResetPressed = btnReset.is_pressed



