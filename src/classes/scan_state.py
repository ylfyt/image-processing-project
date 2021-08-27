import time

class ScanState:
    SCAN_DURATION = 10
    scanStartTime = time.time()
    STATE_INFO = ["idle", "scanning", "reset"]
    state = STATE_INFO[0]
    
    @staticmethod
    def resetScan():
        ScanState.scanStartTime = time.time()
        print("reset")
    
    def getScanTime():
        return time.time() - ScanState.scanStartTime
    
    def getState():
        return ScanState.state

    def setScanningState():
        ScanState.state = ScanState.STATE_INFO[1]
    
    def setIdleState():
        ScanState.state = ScanState.STATE_INFO[0]
    
    def setResetState():
        ScanState.state = ScanState.STATE_INFO[2]
    
    def isResetState():
        return ScanState.state == ScanState.STATE_INFO[2]
    
    def isIdleState():
        return ScanState.state == ScanState.STATE_INFO[0]

    def isScanningState():
        return ScanState.state == ScanState.STATE_INFO[1]
    