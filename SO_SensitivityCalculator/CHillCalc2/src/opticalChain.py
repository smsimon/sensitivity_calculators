#python Version 2.7.2
import numpy as np
import optic as op

class OpticalChain:
    def __init__(self, log, optFile, nrealize=1, optBands=None):
        self.log = log

        #Store optic objects
        output      = np.loadtxt(optFile, dtype=np.str, delimiter='|'); keyArr  = output[0]; elemArr = output[1:]
        opticDicts  = [{keyArr[i].strip(): elem[i].strip() for i in range(len(keyArr))} for elem in elemArr]
        if optBands:
            self.optics = []
            for opticDict in opticDicts:
                if opticDict['Element'] in optBands.keys(): self.optics.append(op.Optic(log, opticDict, nrealize=nrealize, bandFile=optBands[opticDict['Element']]))
                else:                                       self.optics.append(op.Optic(log, opticDict, nrealize=nrealize))
        else:
            self.optics = [op.Optic(log, opticDict, nrealize=nrealize) for opticDict in opticDicts]
            
    #***** Public Methods *****
    #Generate element, temperature, emissivity, and efficiency arrays
    def generate(self, ch):
        arr = [optic.generate(ch) for optic in self.optics]
        elem = [a[0] for a in arr]; emiss = [a[1] for a in arr]; effic = [a[2] for a in arr]; temp = [a[3] for a in arr]
        return elem, emiss, effic, temp
