from time import sleep, time
import datetime
from threading import *
from classes.config import Config
# import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import LED
import cv2
from subprocess import call
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

def onBuzzer(num, delay):
    ScanState.buzzerToggle = buzzerToggle
    ScanState.buzzerDelay = delay
    ScanState.buzzerRepeat = num * 2
    Thread( target=buzzerSignal ).start()

def getPicture(frame, cond):
    current = datetime.datetime.now()
    path = '../img/' + str(current) + '_' + cond + '.jpg'
    cv2.imwrite(path, frame)
    print("Scanned")
    return path

# btnFlashPressed = False
# btnResetPressed = False

def btnControl():
    timerDutarion = Config.getTimerDuration()
    btnResetExitTimer = timerDutarion['exit']
    btnResetShutdownTimer = timerDutarion['shutdown']
    print(btnResetExitTimer)
    print(btnResetShutdownTimer)
    timeCounter = 0
    prevPressed = time()

    while True:
        if btnFlash.is_pressed and btnFlash.is_pressed != ScanState.btnFlashPressed:
            print("btnFlash Was Pressed:")
            ScanState.ledToggle = ledToggle
            Thread( target=ledSwitch ).start()
        ScanState.btnFlashPressed = btnFlash.is_pressed
            
        if btnReset.is_pressed and btnReset.is_pressed != ScanState.btnResetPressed and not ScanState.isState("scanning"):
            print("btnReset Was Pressed:")
            # clear class state
            if (ScanState.isState("picture")):
                onBuzzer(1, 0.5)
                ScanState.setIdleState()
            elif (ScanState.isState("idle")):
                onBuzzer(2, 0.15)
                ScanState.resetScan()
        ScanState.btnResetPressed = btnReset.is_pressed

        if (btnReset.is_pressed):
            timeCounter = time() - prevPressed
            if (timeCounter >= btnResetShutdownTimer):
                print("Shutdown")
                # call("sudo nohup shutdown -h now", shell=True)
                # ScanState.exitProgram = True
        else:
            if (timeCounter >= btnResetExitTimer):
                print("exit")
                # ScanState.exitProgram = True
            timeCounter = 0
            prevPressed = time()
    

        if (ScanState.exitProgram):
            break

        sleep(0.06)
