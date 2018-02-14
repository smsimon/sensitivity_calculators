#python Version 2.7.2
import numpy as np
import units as un

class ScanStrategy:
    def __init__(self, log, scanDict=None, elv=None):
        self.log      = log
        self.scanDict = scanDict
        self.elv      = elv

        if scanDict is not None:
            self.elVals = np.array(scanDict.keys()  ).astype(np.float)
            self.elFrac = np.array(scanDict.values()).astype(np.float)
        else:
            #Default scan strategy
            self.elVals = np.array([30.00, 35.21, 45.52, 47.74, 49.97, 50.00, 52.19, 54.41, 55.00, 56.63, 58.86, 60.00, 61.08, 63.30, 65.52])
            self.elFrac = np.array([10.02, 10.02, 00.82, 00.82, 00.82, 31.99, 00.82, 00.82, 19.85, 00.82, 00.82, 19.87, 00.82, 00.82, 00.82])*un.pctToDec
        
        self.medianElv = 60. #deg
    
    #***** Public Methods *****
    def elvSample(self):
        if self.elv is not None: return self.elv
        else:                    return np.random.choice(self.elVals, size=1, p=self.elFrac/np.sum(self.elFrac))[0]
    def getElv(self):
        return self.elv
    def getMedianElv(self):
        return self.medianElv
