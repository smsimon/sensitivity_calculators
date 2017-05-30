#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import foregrounds as fg
import physics as ph

class Sky:
    def __init__(self, atmFile=None, inclForegrounds=False):
        #***** Private Variables *****
        self.__GHz = 1.e9
        self.__atmFile = atmFile
        self.__inclF = inclForegrounds
        self.__fg = fg.Foregrounds()
        self.__ph = ph.Physics()

        #***** Public Variables *****
        #CMB parameters
        self.Ncmb = 'CMB'
        self.Tcmb = 2.725 #K
        self.Acmb = 1.0
        self.Ecmb = 1.0
        if self.__inclF:
            #Synchrotron parameters
            self.Nsyn = 'SYNC'
            self.Asyn = 1.0
            self.Esyn = 1.0
            #Dust parameters
            self.Ndst = 'DUST'
            self.Adst = 1.0
            self.Edst = 1.0
        if self.__atmFile:
            #Atmosphere parameters
            self.Natm = 'ATM'
            self.Aatm = 1.
            self.freq, self.atmTemp, self.atmTx = np.loadtxt(self.__atmFile, dtype=np.str, unpack=True, usecols=[0, 2, 3])
        
    #***** Private methods *****
    def __atmTrans(self, bandCenter, fbw):
        freqs = []
        trans = []
        temps = []
        fLo = bandCenter*(1. - 0.5*fbw)
        fHi = bandCenter*(1. + 0.5*fbw)
        for i in range(len(self.freq)):
            f = float(self.freq[i])*self.__GHz
            if f > fLo and f < fHi:
                freqs.append(f)
                trans.append(float(self.atmTx[i]))
                temps.append(float(self.atmTemp[i]))
        tr = np.trapz(trans, freqs)/(freqs[-1] - freqs[0])
        tp = np.trapz(temps, freqs)/(freqs[-1] - freqs[0])
        return tr, tp
        
    def __getFreqs(self, bandCenter, fbw, nSample=100): 
        fLo = bandCenter*(1. - 0.5*fbw)
        fHi = bandCenter*(1. + 0.5*fbw)
        return np.linspace(fLo, fHi, nSample)
                
    #***** Public methods *****
    def skyParams(self, bandCenter, fbw):
        #Calculate atmosphere transmission and absorption
        if self.__atmFile:
            self.Eatm, self.Tatm = self.__atmTrans(bandCenter, fbw)
        #Calculate foreground temperatures
        if self.__inclF:
            #Caluclate synchrotron BB temperature
            freqs = self.__getFreqs(bandCenter, fbw)
            syncInt = np.trapz(np.array([fg.syncSpecRad(self.Asyn, f) for f in freqs]), freqs)/(freqs[-1] - freqs[0])
            syncRJT = ph.antennaTemp(syncInt, bandCenter)
            self.Tsyn = ph.antennaToBBTemp(syncRJT, bandCenter)
            #Calculate dust BB temperature
            dustInt = np.trapz(np.array([fg.dustSpecRad(self.Adst, f) for f in freqs]), freqs)/(freqs[-1] - freqs[0])
            dustRJT = ph.antennaTemp(dustInt, bandCenter)
            self.Tdst = ph.antennaToBBTemp(dustRJT, bandCenter)
            
        #Store name, temperature, emissivity, efficiency
        elemArr  = [self.Ncmb]
        emissArr = [self.Acmb]
        effArr   = [self.Ecmb]
        tempArr  = [self.Tcmb]
        if self.__inclF:
            elemArr  += [self.Nsyn, self.Ndst]
            emissArr += [self.Asyn, self.Adst]
            effArr   += [self.Esyn, self.Edst]
            tempArr  += [self.Tsyn, self.Tdst]
        if self.__atmFile:
            elemArr  += [self.Natm]
            emissArr += [self.Aatm]
            effArr   += [self.Eatm]
            tempArr  += [self.Tatm]
        
        return elemArr, emissArr, effArr, tempArr
