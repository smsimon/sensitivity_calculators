#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import physics as ph

class Foregrounds:
    def __init__(self):
        #***** Private variables *****
        self.__GHz = 1.e9
        self.__ph = ph.Physics()
        
        #***** Public variables *****
        #Dust constants, taken from Planck
        self.dustTemp = 19.7       #[K]
        self.dustSpecIndex = 1.5
        self.dustFact = 2.e-3
        self.dustFrequency = 353*self.__GHz #[Hz]

        #Dust angular power spectrum constants, taken from Dunkley
        self.dustAngFact = 8.e-12
        self.dustEll0    = 10.0
        self.dustNu0     = 90.0*self.__GHz #[Hz]
        self.dustM       = -0.5

        #Synchrotron constants
        self.syncSpecIndex = -3.0
        self.syncFact = 6.e3

        #Synchrotron angular power spectrum constants, taken from Dunkley
        self.syncAngFact = 4e-12
        self.syncEll0    = 10.0
        self.syncNu0     = 90.0*self.__GHz #[Hz]
        self.syncM       = -0.6

    #***** Public methods *****
    #Polarized galactic dust spectral radiance [W/(m^2-Hz)]
    def dustSpecRad(self, emissivity, freq, dustFact=None, dustTemp=None, dustSpecIndex=None):
        if dustFact == None:
            dustFact = self.dustFact
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return emissivity*dustFact*((freq/self.dustFrequency)**dustSpecIndex)*self.__ph.bbSpecRad(freq, dustTemp)

    #Polarized galactic dust power spectrum on a diffraction-limited detector [W/Hz]
    def dustPowSpec(self, emissivity, freq, dustFact=None, dustTemp=None, dustSpecIndex=None):
        if dustFact == None:
            dustFact = self.dustFact
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return 0.5*self.__ph.AOmega(freq)*self.dustSpecRad(emissivity, freq, dustFact, dustTemp, dustSpecIndex) 

    #Polarized galactic dust power on a diffraction-limited detector [W]
    def dustPower(self, emissivity, freq, fbw, dustFact=None, dustTemp=None, dustSpecIndex=None):
        if dustFact == None:
            dustFact = self.dustFact
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.dustPowSpec(emissivity(x), x, dustFact, dustTemp, dustSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.dustPowSpec(emissivity,    x, dustFact, dustTemp, dustSpecIndex), freq1, freq2)[0]
    
    #Polarized galactic dust power dust power equivalent CMB temperature spectrum on a diffraction-limited detector [K/Hz]
    def dustPowTempSpec(self, emissivity, freq, dustFact=None, dustTemp=None, dustSpecIndex=None):
        if dustFact == None:
            dustFact = self.dustFact
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return self.dustPowSpec(emissivity, freq, dustFact, dustTemp, dustSpecIndex)/self.__ph.aniPowSpec(emissivity, freq, self.__ph.Tcmb)

    #Polarized galactic dust power dust power equivalent CMB temperature on a diffraction-limited detector [K]
    def dustPowTemp(self, emissivity, freq, fbw, dustFact=None, dustTemp=None, dustSpecIndex=None):
        if dustFact == None:
            dustFact = self.dustFact
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.dustPowTempSpec(emissivity(x), x, dustFact, dustTemp, dustSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.dustPowTempSpec(emissivity   , x, dustFact, dustTemp, dustSpecIndex), freq1, freq2)[0]    

    #Synchrotron spectral radiance [W/(m^2-Hz)]
    def syncSpecRad(self, emissivity, freq, syncFact=None, syncSpecIndex=None):
        if syncFact == None:
            syncFact = self.syncFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        return emissivity*syncFact*(freq**syncSpecIndex)

    #Synchrotron power spectrum on a diffraction-limited detector [W/Hz]
    def syncPowSpec(self, emissivity, freq, syncFact=None, syncSpecIndex=None):
        if syncFact == None:
            syncFact = self.syncFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        return 0.5*self.__ph.AOmega(freq)*self.syncSpecRad(emissivity, freq, syncFact, syncSpecIndex)

    #Synchrotron power on on diffraction-limited detector [W]
    def syncPower(self, emissivity, freq, fbw, syncFact=None, syncSpecIndex=None):
        if syncFact == None:
            syncFact = self.syncFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.syncPowSpec(emissivity(x), x, syncFact, syncSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.syncPowSpec(emissivity,    x, syncFact, syncSpecIndex), freq1, freq2)[0]
        
    #Synchrotron power equivalent CMB temperature spectrum on a diffraction-limited detector [K/Hz]
    def syncPowTempSpec(self, emissivity, freq, syncFact=None, syncSpecIndex=None):
        if syncFact == None:
            syncFact = self.syncFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex
        
        return self.syncPowSpec(emissivity, freq, syncFact, syncSpecIndex)/self.__ph.aniPowSpec(emissivity, freq, self.__ph.Tcmb)

    #Synchrotron power equivalent CMB temperature on a diffraction-limited detector [K]
    def syncPowTemp(self, emissivity, freq, fbw, syncFact=None, syncSpecIndex=None):
        if syncFact == None:
            syncFact = self.syncFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freqCent, fracBw)
        if callable(emissivity):
            return itg.quad(self.syncPowTempSpec(emissivity(x), x, syncFact, syncSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.syncPowTempSpec(emissivity,    x, syncFact, syncSpecIndex), freq1, freq2)[0]
        
    #Polarized galactic dust angular power spectrum [W/Hz]
    def dustAngPowSpec(self, emissivity, freq, ell, dustAngFact=None, dustSpecIndex=None, dustEll0=None, dustNu0=None, dustM=None):
        if dustAngFact == None:
            dustAngFact = self.dustAngFact
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex
        if dustEll0 == None:
            dustEll0 = self.dustEll0
        if dustNu0 == None:
            dustNu0 = self.dustNu0
        if dustM == None:
            dustM = self.dustM

        return emissivity*((2*self.__ph.PI*dustAngFact)/(ell*(ell + 1)))*((freq/dustNu0)**(2*dustSpecIndex))*((ell/dustEll0)**dustM)

    #For calculating the polarized synchrotron radiation angular power spectrum
    def syncAngPowSpec(self, emissivity, freq, ell, syncAngFact=None, syncSpecIndex=None, syncEll0=None, syncNu0=None, syncM=None):
        if syncAngFact == None:
            syncAngFact = self.syncAngFact
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex
        if syncEll0 == None:
            syncEll0 = self.syncEll0
        if syncNu0 == None:
            syncNu0 = self.syncNu0
        if syncM == None:
            syncM = self.syncM

        return emissivity*((2*self.__ph.PI*syncAngFact)/(ell*(ell + 1)))*((freq/syncNu0)**(2*syncSpecIndex))*((ell/syncEll0)**syncM)
