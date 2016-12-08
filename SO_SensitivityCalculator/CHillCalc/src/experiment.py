#!/usr/local/bin/python

#Classes for handling CMB experiments
#class PB2

#python Version 2.7.2
import numpy as np

#Class for handling PB2 parameters
class PB2:
    def __init__(self):
        #***** Private variables *****
        self.__mm     = 1.e-3  #m from mm
        self.__GHz    = 1.e+9  #GHz from Hz
        self.__aWrtHz = 1.e-18 #aW/rtHz from W/rtHz
        self.__pArtHz = 1.e-12 #pA/rtHz from A/rtHz
        self.__Hz     = 1.e-9  #Hz from GHz
        self.__pW     = 1.e-12 #pW from W
        #Directory that holds each band's optical parameters
        self.__opDir = './opticalParams/PB2/'
        
        #***** Public variables *****
        #Experiment name
        self.name = "PB2"
        #Psat/Popt factor
        self.psatFact = 2.5
        #Minimum allowed Pelec/Popt
        self.psatMinFact = 2.0
        #Number of detector modes
        self.nModes = 1.0
        #Thermal carrier power index
        #1.0 for electron, 3.0 for phonon
        self.n = 3
        #Bath Temperature [K] from John G. on 2016-09-15
        self.Tb = 0.280
        #self.Tb = 0.250
        #Transition temperature [K] from Toki on 2016-09-15
        self.Tc = 0.400
        #self.Tc = 1.710*self.Tb #1.710*Tb for n = 3, 2.140*Tb for n = 1
        #Total number of detectors
        #3794 at 90 GHz, 3794 at 150 GHz ; 3794 at 220 GHz and 3794 at 270 GHz
        self.nDet = 7588
        #Noise equivalent current [aW/rtHz] from Darcy on 2016-09-15
        self.nei = 10.*self.__pArtHz
        #Bolometer operating resistance [Ohm]
        self.boloR = 1.0
        #Photon bunching factor
        self.bf = 1.

        #PB2 bands
        #Number of bands
        self.numBands = 4
        #Band ID
        self.bandIDArr = np.array([0, 1, 2, 3])
        #Band names 
        self.bandNameArr = np.array(['wBand', 'dBand', 'sBand', 'qBand'])
        #Band center [Hz]
        self.bandCenterArr = np.array([89.5, 147.8, 220.0, 270.0])*self.__GHz
        #Fractional bandwidth
        self.fbwArr = np.array([0.324, 0.260, 0.200, 0.200])
        #Low frequency [Hz]
        self.loArr = self.bandCenterArr*(1. - 0.5*self.fbwArr)
        #High frequency [Hz]
        self.hiArr = self.bandCenterArr*(1. + 0.5*self.fbwArr)
        #Pixel size [m]
        self.pixSizeArr = np.array([6.8, 6.8, 3.8, 3.8])*self.__mm
        #Number of detectors
        self.nDetArr = np.array([self.nDet/2., self.nDet/2., self.nDet/2., self.nDet/2.])
        #Number of pixels
        self.nPixArr = self.nDetArr/2
        #PWV cuts [mm] as of 2016-09-26
        self.pwvCutArr = np.array([4.0, 3.5, 3.0, 3.0])
        #Psat for each band as of 2016-12-07
        self.psatArr = np.array([8., 14., 20., 26.])*self.__GHz

        #Scan strategy as of 2016-09-15
        #From Neil on 2016-09-15, regarding wedding cake scan strategy
        #PB2a/b
        self.__elVals_PB2ab = np.array([30.,         35.2126,     45.5226,    47.7448,    49.967,      50.,         52.1892, 
                                      54.4114,     55.,         56.6336,    58.8558,    60.,         61.078,      63.3002,    65.5226])
        self.__elFrac_PB2ab = np.array([10.01971083, 10.02028185, 0.82452597, 0.82452597, 0.82452597,  31.98748368, 0.82452597, 
                                      0.82452597,  19.85389884, 0.82452597, 0.82452597, 19.87336505, 0.82452597,  0.82452597, 0.82452597])*0.01
        #PB2c
        self.__elVals_PB2c = np.array([30.,         35.2126,     45.5226,    47.7448,    49.967,      50.,         52.1892, 
                                     54.4114,     55.,         56.6336,    58.8558,    60.,         61.078,      63.3002,    65.5226])
        self.__elFrac_PB2c = np.array([10.01971083, 10.02028185, 0.82452597, 0.82452597, 0.82452597,  31.98748368, 0.82452597, 
                                     0.82452597,  19.85389884, 0.82452597, 0.82452597, 19.87336505, 0.82452597,  0.82452597, 0.82452597])*0.01

        #Lowest elevation values
        self.__elCut_PB2ab = self.__elVals_PB2ab[0]
        self.__elCut_PB2c  = self.__elVals_PB2c[0]

    #***** Public methods *****
    #For finding the band ID from the central frequency
    def bandID(self, bandCenter):
        #If "bandCenter" is in GHz, convert to Hz
        if bandCenter*1.e-9 < 1.0:
            bandCenter = bandCenter*1.0e9

        #Round to the nearest GHz
        GHz = 1.e-9
        rd = 0
    
        #Which band are we analyzing?
        if   np.round(bandCenter*GHz, rd) == np.round(self.wBandCenter*GHz, rd):
            return self.dBandID
        elif np.round(bandCenter*GHz, rd) == np.round(self.dBandCenter*GHz, rd):
            return self.wBandID
        elif np.round(bandCenter*GHz, rd) == np.round(self.sBandCenter*GHz, rd):
            return self.sBandID
        elif np.round(bandCenter*GHz, rd) == np.round(self.qBandCenter*GHz, rd):
            return self.qBandID
        else:
            print "pb2.whichBand() cannot determine band number. Using '1' for 150 GHz"
            return 1

    #Retrive band optical parameters, assuming no HWP
    def bandParams(self, bandID):
        if   bandID == self.bandIDArr[0]:
            f = self.__opDir+"wBandOpticalParams.txt"
        elif bandID == self.bandIDArr[1]:
            f = self.__opDir+"dBandOpticalParams.txt"
        elif bandID == self.bandIDArr[2]:
            f = self.__opDir+"sBandOpticalParams.txt"
        elif bandID == self.bandIDArr[3]:
            f = self.__opDir+"qBandOpticalParams.txt"
        elems             = np.loadtxt(f, dtype=np.str,   usecols=[0],     unpack=True, skiprows=1) 
        emms, effs, temps = np.loadtxt(f, dtype=np.float, usecols=[1,2,3], unpack=True, skiprows=1)
        
        return elems, emms, effs, temps
    
    #Retrive band optical parameters, assuming a HWP
    def bandParams_HWP(self, bandID):
        if   bandID == self.bandIDArr[1]:
            f = self.__opDir+"wBandOpticalParams_withHWP.txt"
        elif bandID == self.bandIDArr[2]:
            f = self.__opDir+"dBandOpticalParams_withHWP.txt"
        elif bandID == self.bandIDArr[3]:
            f = self.__opDir+"sBandOpticalParams_withHWP.txt"
        elif bandID == self.bandIDArr[4]:
            f = self.__opDir+"qBandOpticalParams_withHWP.txt"
        elems             = np.loadtxt(f, dtype=np.str,   usecols=[0],     unpack=True, skiprows=1) 
        emms, effs, temps = np.loadtxt(f, dtype=np.float, usecols=[1,2,3], unpack=True, skiprows=1)
        
        return elems, emms, effs, temps

    #Method to return PWV cut for each band
    def pwvCut(self):
        return self.__wPwvCut, self.__dPwvCut, self.__sPwvCut, self.__qPwvCut

    #Method to return El cut for PB2ab and PB2c
    def elCut(self):
        return self.__elCut_PB2ab, self.__elCut_PB2c
    
    #Function that returns elevation pdf for PB2ab and PB2c
    def elBaseDist(self):
        return self.__elVals_PB2ab, self.__elFrac_PB2ab, self.__elVals_PB2c, self.__elFrac_PB2c

    #Method for return the CES elevation distribution for PB2ab and PB2c
    def elDist(self, nSamples=100):
        return np.random.choice(self.__elVals_PB2ab,  size=nSamples, p=self.__elFrac_PB2ab), np.random.choice(self.__elVals_PB2c,  size=nSamples, p=self.__elFrac_PB2c)

    #Method to return data selection efficiency vs PWV
    def dsVsPwv(self, pwv):
        return 1.0 - 0.072*pwv
