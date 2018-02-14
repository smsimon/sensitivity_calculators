#python Version 2.7.2
import numpy     as np
import physics   as ph
import units     as un
import parameter as pr

class Foregrounds:
    def __init__(self, fgndDict=None, nrealize=1):
        self.__ph = ph.Physics()

        #Sample the foreground parameters
        if fgndDict:
            def samp(param, pos=False, norm=False): 
                if nrealize == 1: return param.getAvg()
                else:             return param.sample(nsample=1, pos=pos, norm=norm)
            self.dustTemp      = samp(pr.Parameter(fgndDict['Dust Temperature']),       pos=True)
            self.dustSpecIndex = samp(pr.Parameter(fgndDict['Dust Spec Index'])                 )
            self.dustAmp       = samp(pr.Parameter(fgndDict['Dust Amplitude']),         pos=True)
            self.dustFrequency = samp(pr.Parameter(fgndDict['Dust Scale Frequency']),   pos=True)
            self.syncSpecIndex = samp(pr.Parameter(fgndDict['Synchrotron Spec Index'])          )
            self.syncAmp       = samp(pr.Parameter(fgndDict['Synchrotron Amplitude']),  pos=True)
        else:
            #Dust constants, taken from Planck
            self.dustTemp = 19.7       #[K]
            self.dustSpecIndex = 1.5
            self.dustAmp = 2.e-3
            self.dustFrequency = 353*un.GHzToHz #[Hz]
            #Synchrotron constants
            self.syncSpecIndex = -3.0
            self.syncAmp = 6.e3

        #Dust angular power spectrum constants, taken from Dunkley
        self.dustAngAmp = 8.e-12
        self.dustEll0    = 10.0
        self.dustNu0     = 90.0*un.GHzToHz #[Hz]
        self.dustM       = -0.5

        #Synchrotron angular power spectrum constants, taken from Dunkley
        self.syncAngAmp = 4e-12
        self.syncEll0    = 10.0
        self.syncNu0     = 90.0*un.GHzToHz #[Hz]
        self.syncM       = -0.6

    #***** Public methods *****
    #Polarized galactic dust spectral radiance [W/(m^2-Hz)]
    def dustSpecRad(self, emissivity, freq, dustAmp=None, dustTemp=None, dustSpecIndex=None):
        if dustAmp == None:
            dustAmp = self.dustAmp
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return emissivity*dustAmp*((freq/self.dustFrequency)**dustSpecIndex)*self.__ph.bbSpecRad(freq, dustTemp)

    #Polarized galactic dust power spectrum on a diffraction-limited detector [W/Hz]
    def dustPowSpec(self, emissivity, freq, dustAmp=None, dustTemp=None, dustSpecIndex=None):
        if dustAmp == None:
            dustAmp = self.dustAmp
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return 0.5*self.__ph.AOmega(freq)*self.dustSpecRad(emissivity, freq, dustAmp, dustTemp, dustSpecIndex) 

    #Polarized galactic dust power on a diffraction-limited detector [W]
    def dustPower(self, emissivity, freq, fbw, dustAmp=None, dustTemp=None, dustSpecIndex=None):
        if dustAmp == None:
            dustAmp = self.dustAmp
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.dustPowSpec(emissivity(x), x, dustAmp, dustTemp, dustSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.dustPowSpec(emissivity,    x, dustAmp, dustTemp, dustSpecIndex), freq1, freq2)[0]
    
    #Polarized galactic dust power dust power equivalent CMB temperature spectrum on a diffraction-limited detector [K/Hz]
    def dustPowTempSpec(self, emissivity, freq, dustAmp=None, dustTemp=None, dustSpecIndex=None):
        if dustAmp == None:
            dustAmp = self.dustAmp
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        return self.dustPowSpec(emissivity, freq, dustAmp, dustTemp, dustSpecIndex)/self.__ph.aniPowSpec(freq, self.__ph.Tcmb, emissivity)

    #Polarized galactic dust power dust power equivalent CMB temperature on a diffraction-limited detector [K]
    def dustPowTemp(self, emissivity, freq, fbw, dustAmp=None, dustTemp=None, dustSpecIndex=None):
        if dustAmp == None:
            dustAmp = self.dustAmp
        if dustTemp == None:
            dustTemp = self.dustTemp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.dustPowTempSpec(emissivity(x), x, dustAmp, dustTemp, dustSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.dustPowTempSpec(emissivity   , x, dustAmp, dustTemp, dustSpecIndex), freq1, freq2)[0]    

    #Synchrotron spectral radiance [W/(m^2-Hz)]
    def syncSpecRad(self, emissivity, freq, syncAmp=None, syncSpecIndex=None):
        if syncAmp == None:
            syncAmp = self.syncAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        return emissivity*syncAmp*(freq**syncSpecIndex)

    #Synchrotron power spectrum on a diffraction-limited detector [W/Hz]
    def syncPowSpec(self, emissivity, freq, syncAmp=None, syncSpecIndex=None):
        if syncAmp == None:
            syncAmp = self.syncAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        return 0.5*self.__ph.AOmega(freq)*self.syncSpecRad(emissivity, freq, syncAmp, syncSpecIndex)

    #Synchrotron power on on diffraction-limited detector [W]
    def syncPower(self, emissivity, freq, fbw, syncAmp=None, syncSpecIndex=None):
        if syncAmp == None:
            syncAmp = self.syncAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freq, fbw)
        if callable(emissivity):
            return itg.quad(self.syncPowSpec(emissivity(x), x, syncAmp, syncSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.syncPowSpec(emissivity,    x, syncAmp, syncSpecIndex), freq1, freq2)[0]
        
    #Synchrotron power equivalent CMB temperature spectrum on a diffraction-limited detector [K/Hz]
    def syncPowTempSpec(self, emissivity, freq, syncAmp=None, syncSpecIndex=None):
        if syncAmp == None:
            syncAmp = self.syncAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex
        
        return self.syncPowSpec(emissivity, freq, syncAmp, syncSpecIndex)/self.__ph.aniPowSpec(freq, self.__ph.Tcmb, emissivity)

    #Synchrotron power equivalent CMB temperature on a diffraction-limited detector [K]
    def syncPowTemp(self, emissivity, freq, fbw, syncAmp=None, syncSpecIndex=None):
        if syncAmp == None:
            syncAmp = self.syncAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex

        freq1, freq2 = self.__ph.bandEdges(freqCent, fracBw)
        if callable(emissivity):
            return itg.quad(self.syncPowTempSpec(emissivity(x), x, syncAmp, syncSpecIndex), freq1, freq2)[0]
        else:
            return itg.quad(self.syncPowTempSpec(emissivity,    x, syncAmp, syncSpecIndex), freq1, freq2)[0]
        
    #Polarized galactic dust angular power spectrum [W/Hz]
    def dustAngPowSpec(self, emissivity, freq, ell, dustAngAmp=None, dustSpecIndex=None, dustEll0=None, dustNu0=None, dustM=None):
        if dustAngAmp == None:
            dustAngAmp = self.dustAngAmp
        if dustSpecIndex == None:
            dustSpecIndex = self.dustSpecIndex
        if dustEll0 == None:
            dustEll0 = self.dustEll0
        if dustNu0 == None:
            dustNu0 = self.dustNu0
        if dustM == None:
            dustM = self.dustM

        return emissivity*((2*self.__ph.PI*dustAngAmp)/(ell*(ell + 1)))*((freq/dustNu0)**(2*dustSpecIndex))*((ell/dustEll0)**dustM)

    #For calculating the polarized synchrotron radiation angular power spectrum
    def syncAngPowSpec(self, emissivity, freq, ell, syncAngAmp=None, syncSpecIndex=None, syncEll0=None, syncNu0=None, syncM=None):
        if syncAngAmp == None:
            syncAngAmp = self.syncAngAmp
        if syncSpecIndex == None:
            syncSpecIndex = self.syncSpecIndex
        if syncEll0 == None:
            syncEll0 = self.syncEll0
        if syncNu0 == None:
            syncNu0 = self.syncNu0
        if syncM == None:
            syncM = self.syncM

        return emissivity*((2*self.__ph.PI*syncAngAmp)/(ell*(ell + 1)))*((freq/syncNu0)**(2*syncSpecIndex))*((ell/syncEll0)**syncM)
