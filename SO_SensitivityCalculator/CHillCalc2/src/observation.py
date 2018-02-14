#python Version 2.7.2
import numpy as np

class Observation:
    def __init__(self, log, detArray, sky, scn):
        self.sky = sky
        self.scn = scn

        #Sample PWV and Elevation
        self.pwv = self.sky.pwvSample()
        self.elv = self.scn.elvSample()
                    
        #Sample and store sky optical parameters
        elem, emiss, effic, temp = np.hsplit(np.array([self.sky.generate(self.pwv, self.elv, det.ch.freqs) for det in detArray.detectors]), 4)
        self.elem  = elem.reshape( len(elem),  len(elem[0][0]),  len(elem[0][0][0])).astype(np.str  );  self.elem  = np.array(self.elem,  order='F'); self.elem.resize(len(self.elem), len(self.elem[0])); self.elem  = self.elem.tolist()
        self.emiss = emiss.reshape(len(emiss), len(emiss[0][0]), len(emiss[0][0][0])).astype(np.float);                                                                                                    self.emiss = self.emiss.tolist()
        self.effic = effic.reshape(len(effic), len(effic[0][0]), len(effic[0][0][0])).astype(np.float);                                                                                                    self.effic = self.effic.tolist()
        self.temp  = temp.reshape( len(temp),  len(temp[0][0]),  len(temp[0][0][0])).astype(np.float);                                                                                                     self.temp  = self.temp.tolist()
