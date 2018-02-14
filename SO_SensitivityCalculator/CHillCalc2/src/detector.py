#python Version 2.7.2
import numpy     as np
import parameter as pr
import units     as un
import physics   as ph

class Detector:
    def __init__(self, log, ch, band=None):
        self.log  = log
        self.ch   = ch
        self.__ph = ph.Physics()

        #Sample detector parameters
        def samp(param, bandID=ch.bandID, pos=False, norm=False, min=None, max=None): 
            if ch.clcDet == 1: return param.getAvg(bandID)
            else:              return param.sample(bandID=bandID, nsample=1, pos=pos, norm=norm, min=min, max=max)
        self.bandCenter    = samp(pr.Parameter(ch.dict['Band Center'], un.GHzToHz),     pos=True)
        self.fbw           = samp(pr.Parameter(ch.dict['Fractional BW']),               pos=True, norm=True)
        self.flo, self.fhi = self.__ph.bandEdges(self.bandCenter, self.fbw)
        self.detEff        = samp(pr.Parameter(ch.dict['Det Eff']),                     pos=True, norm=True)*ch.optCouple
        self.psat          = samp(pr.Parameter(ch.dict['Psat'], un.pWtoW),              pos=True)
        self.psatFact      = samp(pr.Parameter(ch.dict['Psat Factor']),                 pos=True)
        self.n             = samp(pr.Parameter(ch.dict['Carrier Index']),               pos=True)
        self.Tb            = ch.Tb
        self.Tc            = samp(pr.Parameter(ch.dict['Tc']),                          min=self.Tb+0.001)
        self.TcFrac        = samp(pr.Parameter(ch.dict['Tc Fraction']),                 min=1.01)
        if 'NA' in str(self.Tc): self.Tc = self.Tb*self.TcFrac
        self.nei           = samp(pr.Parameter(ch.dict['SQUID NEI'], un.pArtHzToArtHz), pos=True)
        self.boloR         = samp(pr.Parameter(ch.dict['Bolo Resistance']),             pos=True)
        self.readN         = samp(pr.Parameter(ch.dict['Read Noise Frac']),             pos=True)

        #Load band
        if band is not None:
            eff  = band
            if eff is not None:
                eff = np.array([e if e > 0 else 0. for e in eff])
                eff = np.array([e if e < 1 else 1. for e in eff])
        else: 
            #Default to top hat band
            eff = [self.detEff if f > self.flo and f < self.fhi else 0. for f in ch.freqs]

        #Store detector optical parameters
        self.elem  = ["Detector"]
        self.emiss = [[0.000 for f in ch.freqs]]
        self.effic = [eff]
        self.temp  = [[self.Tb for f in ch.freqs]]
