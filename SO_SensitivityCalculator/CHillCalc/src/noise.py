#!/usr/local/bin/python

#Classes for handling noise calculations
#class Noise

#python Version 2.7.2
import numpy as np
import scipy.integrate as itg
import physics as phy
import experiment as exp

#Class for noise
class Noise:
    def __init__(self):        
        #***** Private variables *****
        self.__ph  = phy.Physics()
        self.__pb2 = exp.PB2()
        
        #Efficiency of the cosmos
        self.__skyEff = 1.
        #Bunching factor
        self.__bf = 1.
        
    #Photon noise equivalent power on a diffraction-limited detector [W/rtHz]
    def photonNEP(self, poptArr, freq=None, fbw=None, bf=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.wFbw
        if bf == None:
            bf = self.__bf

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        popt  = lambda f: sum([x(f) for x in poptArr])
        popt2 = lambda f: sum([x(f)*y(f) for x in poptArr for y in poptArr])
        return np.sqrt(itg.quad(lambda x: 2*self.__ph.h*x*popt(x) + 2*bf*popt2(x), freq1, freq2)[0])

    #8% overestimate of photon noise equivalent power on a diffraction-limited detector [W/rt(Hz)]
    def photonNEPapprox(self, pow, freq=None, fbw=None, bf=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.wFbw
        if bf == None:
            bf = self.__bf

        deltaF = freq*fbw
        return np.sqrt(2*(self.__ph.h*freq*pow + bf*((pow**2)/deltaF)))

    #Bolometer noise equivalent power [W/rt(Hz)]
    def bolometerNEP(self, psat, n=None, Tc=None, Tb=None):
        if n == None:
            n = self.__pb2.n
        if Tc == None:
            Tc = self.__pb2.Tc
        if Tb == None:
            Tb = self.__pb2.Tb
        return np.sqrt(4*self.__ph.kB*psat*Tb*(((np.power((n+1),2.)/((2*n)+3))*((np.power((Tc/Tb),((2*n)+3)) - 1)/np.power((np.power((Tc/Tb),(n+1)) - 1),2.)))))

    #Readout noise equivalent power [W/rt(Hz)]
    def readoutNEP(self, pelec, boloR=None, nei=None):
        if boloR == None:
            boloR = self.__pb2.boloR
        if nei == None:
            nei = self.__pb2.nei

        return np.sqrt(boloR*pelec)*nei

    #Change in power with change in CMB temperature [W/K]
    def dPdT(self, emissivity, freq=None, fbw=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        return self.__ph.aniPower(emissivity, freq, fbw, self.__ph.Tcmb)
    
    #Photon noise equivalent temperature [K-rtSec]
    def photonNET(self, poptArr, freq=None, fbw=None, bf=None, skyEff=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        if bf == None:
            bf = self.__bf
        if skyEff == None:
            skyEff = self.__skyEff

        nep  = self.photonNEP(poptArr, freq, fbw, bf)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #8% overestimate of photon noise equivalent tempeature [K-rtSec]
    def photonNETapprox(self, pow, freq=None, fbw=None, bf=None, skyEff=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        if bf == None:
            bf = self.__bf
        if skyEff == None:
            skyEff = self.__skyEff

        nep  = photonNEPapprox(pow, freq, fbw, bf)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Bolometer noise equivalent temperature [K-rtSec]
    def bolometerNET(self, psat, freq=None, fbw=None, n=None, Tc=None, Tb=None, skyEff=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        if n == None:
            n = self.__pb2.n
        if Tc == None:
            Tc = self.__pb2.Tc
        if Tb == None:
            Tb = self.__pb2.Tb
        if skyEff == None:
            skyEff = self.__skyEff

        nep  = bolometerNEP(psat, n, Tc, Tb) 
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Readout noise equivalent temperature [K-rtSec]
    def readoutNET(self, pelec, freq=None, fbw=None, boloR=None, nei=None, skyEff=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        if boloR == None:
            boloR = self.__pb2.boloR
        if nei == None:
            nei = self.__pb2.nei
        if skyEff == None:
            skyEff = self.skyEff

        nep  = readoutNEP(pelec, boloR, nei)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Total noise equivalent temperature [K-rtSec]
    def NETfromNEP(self, nep, freq=None, fbw=None, skyEff=None):
        if freq == None:
            freq = self.__pb2.dBandCenter
        if fbw == None:
            fbw = self.__pb2.dFbw
        if skyEff == None:
            skyEff = self.__skyEff

        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Array noise equivalent temperature [K-rtSec]
    def NETarr(self, net, nDet=None, detYield=None):
        if nDet == None:
            nDet = self.__pb2.nDet
        if detYield == None:
            detYield = 1.0
        
        return net/np.sqrt(nDet*detYield)
    
    #Sky sensitivity [K-arcmin]
    def sensitivity(self, netArr, fsky, tobs):
        return np.sqrt((4.*self.__ph.PI*fsky*2.*np.power(netArr, 2.))/tobs)*(10800./self.__ph.PI)

    #Mapping speed [(K^2*sec)^-1]
    def mappingSpeed(self, net, nDet=None, detYield=None):
        if nDet == None:
            nDet = self.__pb2.nDet
        if detYield == None:
            detYield = 1.0

        return detYield/np.power(self.NETarr(net, nDet), 2.)
