import time

class ScanState:
    SCAN_DURATION = 5
    TAKE_PICTURE_DELAY = 1
    scanStartTime = time.time()
    STATE_INFO = ["idle", "scanning", "picture"]
    state = STATE_INFO[0]
    btnResetPressed = False
    btnFlashPressed = False
    ledFlag = False

    ledToggle = 1
    buzzerToggle = 1
    buzzerDelay = 0.5
    buzzerRepeat = 4
    
    @staticmethod
    def resetScan():
        ScanState.scanStartTime = time.time()
        ScanState.setScanningState()
    
    def getScanTime():
        return time.time() - ScanState.scanStartTime
    
    def getState():
        return ScanState.state

    def setScanningState():
        ScanState.state = ScanState.STATE_INFO[1]
    
    def setIdleState():
        ScanState.state = ScanState.STATE_INFO[0]
    
    def setPictureState():
        ScanState.state = ScanState.STATE_INFO[2]
    
    def isState(st):
        return ScanState.state == st
    