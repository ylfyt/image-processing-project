from time import sleep, time
import datetime
from threading import *
# import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import LED
import cv2
from classes.scan_state import ScanState


# GPIO.setmode(GPIO.BOARD)
btnFlash=Button(12)     # flash
btnPhoto=20      # take photo
btnReset= Button(16)
ledToggle = LED(20)           # LED
buzzerToggle = LED(21)
# GPIO.setup(btnFlash,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnPhoto,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnReset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED,GPIO.OUT)
# GPIO.setup(BUZZER,GPIO.OUT)
flagLED=False
flagBuzzer=False


# class state

def buzzerSignal():
    flagSignal = False
    for i in range(ScanState.buzzerRepeat):
        if flagSignal==False:
            ScanState.buzzerToggle.on()
            flagSignal=True
            sleep(ScanState.buzzerDelay)
        else:
            ScanState.buzzerToggle.off()
            flagSignal=False
            sleep(ScanState.buzzerDelay)

def ledSwitch():
    if (ScanState.ledFlag == False):
        ScanState.ledToggle.on()
    else:
        ScanState.ledToggle.off()
    ScanState.ledFlag = not ScanState.ledFlag

def getPicture(frame, cond):
    path = '../img/' + '{%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '_' + cond + '.jpg'
    cv2.imwrite(path, frame)
    print("Scanned")
    return path

# btnFlashPressed = False
# btnResetPressed = False

def btnControl():
    if btnFlash.is_pressed and btnFlash.is_pressed != ScanState.btnFlashPressed:
        print("btnFlash Was Pressed:")
        ScanState.ledToggle = ledToggle
        Thread( target=ledSwitch ).start()
    ScanState.btnFlashPressed = btnFlash.is_pressed
        
    if btnReset.is_pressed and btnReset.is_pressed != ScanState.btnResetPressed and not ScanState.isState("scanning"):
        print("btnReset Was Pressed:")
        # clear class state
        if (ScanState.isState("picture")):
            ScanState.buzzerToggle = buzzerToggle
            ScanState.buzzerDelay = 0.2
            ScanState.buzzerRepeat = 4
            Thread( target=buzzerSignal ).start()
            ScanState.setIdleState()
        elif (ScanState.isState("idle")):
            ScanState.buzzerToggle = buzzerToggle
            ScanState.buzzerDelay = 0.5
            ScanState.buzzerRepeat = 2
            Thread( target=buzzerSignal ).start()
            ScanState.resetScan()
    ScanState.btnResetPressed = btnReset.is_pressed

