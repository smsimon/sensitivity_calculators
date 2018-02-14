#python Version 2.7.2
import numpy          as np
import detectorArray  as da
import observationSet as os
import parameter      as pr
import units          as un

class Channel:
    def __init__(self, log, channelDict, camera, optChain, sky, scn, detBandDict=None, nrealize=1, nobs=1, clcDet=1, specRes=1.e9):
        self.log         = log
        self.dict        = channelDict
        self.camera      = camera
        self.optChain    = optChain
        self.sky         = sky
        self.scn         = scn
        self.detBandDict = detBandDict
        self.nobs        = nobs
        self.specRes     = specRes
        
        #Name this channel
        self.bandID    = int(self.dict['Band ID'])
        self.pixelID   = int(self.dict['Pixel ID'])
        self.name      = self.camera.name+str(self.bandID)
        
        #Sample the channel parameters
        def samp(param, bandID=self.bandID, pos=False, norm=False, min=None, max=None): 
            if nrealize == 1: return param.getAvg(bandID)
            else:             return param.sample(bandID=bandID, nsample=1, pos=pos, norm=norm, min=min, max=max)
        self.numDetWaf = int(samp(pr.Parameter(self.dict['Num Det per Wafer']), pos=True))
        self.numWafOT  = int(samp(pr.Parameter(self.dict['Num Waf per OT']),    pos=True))
        self.numOT     = int(samp(pr.Parameter(self.dict['Num OT']),            pos=True))
        self.numDet    = int(self.numDetWaf*self.numWafOT*self.numOT)
        if clcDet == None: self.clcDet = self.numDet
        else:              self.clcDet = clcDet
        self.numPix    = self.numDet/2
        self.detYield  = samp(pr.Parameter(self.dict['Yield']), pos=True, norm=True) #Only one yield per experimental realization

        #Store the camera parameters
        self.optCouple = camera.opticalCouplingToFP
        self.Fnumber   = camera.fnumber
        self.Tb        = camera.Tb        

        #Store the detector parameters
        self.bandCenter    = pr.Parameter(self.dict['Band Center'], un.GHzToHz)
        self.fbw           = pr.Parameter(self.dict['Fractional BW'])

        #Frequencies to integrate over -- wider than nominal band by 30% to cover tolerances/errors
        self.fres          = specRes
        self.freqs         = np.arange(self.bandCenter.getAvg()*(1. - 0.65*self.fbw.getAvg()), self.bandCenter.getAvg()*(1. + 0.65*self.fbw.getAvg()), self.fres)
        self.deltaF        = self.freqs[-1] - self.freqs[0]
        
        #Band mask
        self.fLo           = self.bandCenter.getAvg()*(1. - 0.50*self.fbw.getAvg())
        self.fHi           = self.bandCenter.getAvg()*(1. + 0.50*self.fbw.getAvg())
        self.bandMask      = np.array([1. if f >= self.fLo and f <= self.fHi else 0. for f in self.freqs])
        self.bandDeltaF    = self.fHi - self.fLo
        
        #Sample the pixel parameters
        self.pixSize    = samp(pr.Parameter(self.dict['Pixel Size'], un.mmToM), pos=True)
        self.wf         = samp(pr.Parameter(self.dict['Waist Factor']),         pos=True, min=2.)
        self.apEff      = None #Calculated later
        self.edgeTaper  = None #Calculated later

        #Store the detector array object
        if self.detBandDict and self.name in self.detBandDict.keys(): self.detArray = da.DetectorArray(self.log, self, self.detBandDict[self.name])
        else:                                                         self.detArray = da.DetectorArray(self.log, self)

        #Store the observation set object
        self.obsSet = os.ObservationSet(self.log, self.detArray, self.sky, self.scn, nobs=self.nobs)
        
        #Build the element, emissivity, efficiency, and temperature arrays
        optElem, optEmiss, optEffic, optTemp = self.optChain.generate(self)
        self.elem  = np.array([[obs.elem[i]  + optElem  + self.detArray.detectors[i].elem   for i in range(self.detArray.nDet)] for obs in self.obsSet.observations]).astype(np.str)
        self.emiss = np.array([[obs.emiss[i] + optEmiss + self.detArray.detectors[i].emiss  for i in range(self.detArray.nDet)] for obs in self.obsSet.observations]).astype(np.float)
        self.effic = np.array([[obs.effic[i] + optEffic + self.detArray.detectors[i].effic  for i in range(self.detArray.nDet)] for obs in self.obsSet.observations]).astype(np.float)
        self.temp  = np.array([[obs.temp[i]  + optTemp  + self.detArray.detectors[i].temp   for i in range(self.detArray.nDet)] for obs in self.obsSet.observations]).astype(np.float)
