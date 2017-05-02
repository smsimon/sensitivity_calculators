#!/usr/local/bin/python

#Classes for handling noise calculations
#class Noise

#python Version 2.7.2
import numpy as np
import scipy.integrate as itg
import physics as phy
import experiment as exp
import pickle as pkl

#Class for noise
class Noise:
    def __init__(self):        
        #***** Private variables *****
        self.__ph  = phy.Physics()
        
        #Efficiency of the cosmos
        self.__skyEff = 1.
        #Bunching factor
        self.__bf = 1.

        #Correlation files
        dir = '/'.join(__file__.split('/')[:-1])+'/detCorrFiles/PKL/'
        self.p_c_apert, self.c_apert = pkl.load(open(dir+'coherentApertCorr.pkl',   'rb'))
        self.p_c_stop,  self.c_stop  = pkl.load(open(dir+'coherentStopCorr.pkl',    'rb'))
        self.p_i_apert, self.i_apert = pkl.load(open(dir+'incoherentApertCorr.pkl', 'rb'))
        self.p_i_stop,  self.i_stop  = pkl.load(open(dir+'incoherentStopCorr.pkl',  'rb'))
        self.DetP = self.p_c_apert
        #Correlation factor for hex packing
        #self.corrFact = 3
        self.corrFact = 6

    #Photon noise equivalent power on a diffraction-limited detector [W/rtHz]
    def photonNEP(self, poptArr, freq, fbw, elemArr=None, nDet=None, detPitchFlamb=None):
        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        popt  = lambda f: sum([x(f) for x in poptArr])
        
        #Don't consider correlations
        if elemArr == None and nDet == None:
            popt2  = lambda f: sum([x(f)*y(f) for x in poptArr for y in poptArr])
            nep    = np.sqrt(itg.quad(lambda x: 2*self.__ph.h*x*popt(x) + 2*popt2(x), freq1, freq2)[0])
            neparr = nep
            return nep, neparr
        #Consider correlations
        else:
            FlambMax = 3. #Look for correlations out to this length scale
            ndets = int(round(FlambMax/float(detPitchFlamb), 0))
            inds1 = [np.argmin(abs(np.array(self.DetP) - detPitchFlamb*(n+1)            )) for n in range(ndets)]
            inds2 = [np.argmin(abs(np.array(self.DetP) - detPitchFlamb*(n+1)*np.sqrt(3.))) for n in range(ndets)]
            inds  = np.sort(inds1 + inds2)
            c_apert = np.sum([abs(self.c_apert)[ind] for ind in inds])
            i_apert = np.sum([abs(self.c_apert)[ind] for ind in inds])
            i_stop  = np.sum([abs(self.c_stop)[ ind] for ind in inds])
            c_apert  = np.sqrt(c_apert*self.corrFact + 1.)
            i_apert  = np.sqrt(i_apert*self.corrFact + 1.)
            i_stop   = np.sqrt(i_stop*self.corrFact  + 1.)
            atDet = False
            factors = []
            for i in range(len(elemArr)):
                if 'CMB' in elemArr[i]:
                    factors.append(c_apert)
                if ('Apert' in elemArr[i]) or ('Lyot' in elemArr[i]) or ('Stop' in elemArr[i]):
                    factors.append(i_stop)
                    atDet = True
                elif not atDet:
                    factors.append(i_apert)
                else:
                    factors.append(1.)
            factors = np.array(factors[:-1])
            popt2    = lambda f: sum([poptArr[i](f)*poptArr[j](f)                       for i in range(len(poptArr)) for j in range(len(poptArr))])
            popt2arr = lambda f: sum([factors[i]*factors[j]*poptArr[i](f)*poptArr[j](f) for i in range(len(poptArr)) for j in range(len(poptArr))])
            nep    = np.sqrt(itg.quad(lambda x: 2*self.__ph.h*x*popt(x) + 2*popt2(x),    freq1, freq2)[0])
            neparr = np.sqrt(itg.quad(lambda x: 2*self.__ph.h*x*popt(x) + 2*popt2arr(x), freq1, freq2)[0])
            return nep, neparr

    #8% overestimate of photon noise equivalent power on a diffraction-limited detector [W/rt(Hz)]
    def photonNEPapprox(self, pow, freq, fbw, bf=1.0):
        deltaF = freq*fbw
        return np.sqrt(2*(self.__ph.h*freq*pow + bf*((pow**2)/deltaF)))

    #Bolometer noise equivalent power [W/rt(Hz)]
    def bolometerNEP(self, psat, n, Tc, Tb):
        return np.sqrt(4*self.__ph.kB*psat*Tb*(((np.power((n+1),2.)/((2*n)+3))*((np.power((Tc/Tb),((2*n)+3)) - 1)/np.power((np.power((Tc/Tb),(n+1)) - 1),2.)))))

    #Readout noise equivalent power [W/rt(Hz)]
    def readoutNEP(self, pelec, boloR, nei):
        return np.sqrt(boloR*pelec)*nei

    #Change in power with change in CMB temperature [W/K]
    def dPdT(self, emissivity, freq, fbw):
        return self.__ph.aniPower(emissivity, freq, fbw, self.__ph.Tcmb)
    
    #Photon noise equivalent temperature [K-rtSec]
    def photonNET(self, poptArr, freq, fbw, bf=1.0, skyEff=1.0):
        nep  = self.photonNEP(poptArr, freq, fbw, bf)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #8% overestimate of photon noise equivalent tempeature [K-rtSec]
    def photonNETapprox(self, pow, freq, fbw, bf=1.0, skyEff=1.0):
        nep  = photonNEPapprox(pow, freq, fbw, bf)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Bolometer noise equivalent temperature [K-rtSec]
    def bolometerNET(self, psat, freq, fbw, n, Tc, Tb, skyEff=1.0):
        nep  = bolometerNEP(psat, n, Tc, Tb) 
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Readout noise equivalent temperature [K-rtSec]
    def readoutNET(self, pelec, freq, fbw, boloR, nei, skyEff=1.0):
        nep  = readoutNEP(pelec, boloR, nei)
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Total noise equivalent temperature [K-rtSec]
    def NETfromNEP(self, nep, freq, fbw, skyEff=1.0):
        dpdt = self.dPdT(skyEff, freq, fbw)
        return nep/(np.sqrt(2.)*dpdt)

    #Array noise equivalent temperature [K-rtSec]
    def NETarr(self, net, nDet, detYield=1.0):
        return net/np.sqrt(nDet*detYield)
    
    #Sky sensitivity [K-arcmin]
    def sensitivity(self, netArr, fsky, tobs):
        return np.sqrt((4.*self.__ph.PI*fsky*2.*np.power(netArr, 2.))/tobs)*(10800./self.__ph.PI)

    #Mapping speed [(K^2*sec)^-1]
    def mappingSpeed(self, net, nDet, detYield=1.0):
        return detYield/np.power(self.NETarr(net, nDet), 2.)
