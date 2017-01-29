#!/usr/local/bin/python

#Class for handling CMB experiments

#python Version 2.7.2
import numpy as np

#Function that returns a PB2 class
def PB2():
    #Locate parameter files
    expParamDir   = "./experimentParams/PB2/"
    optParamDir   = "./opticalParams/PB2/"
    expParamFile  = expParamDir+"PB2_expParams.txt"
    optParamFiles = [optParamDir+"PB2_90GHzOpticalParams.txt",
                     optParamDir+"PB2_150GHzOpticalParams.txt",
                     optParamDir+"PB2_220GHzOpticalParams.txt",
                     optParamDir+"PB2_280GHzOpticalParams.txt"]
    return Experiment("PB2", expParamFile, optParamFiles)

#Function that returns an ACTPol class
def ACTPol():
    #Locate parameter files
    expParamDir   = "./experimentParams/ACTPol/"
    optParamDir   = "./opticalParams/ACTPol/"
    expParamFile  = expParamDir+"ACTPol_expParams.txt"
    optParamFiles = [optParamDir+"ACTPol_150GHzOpticalParams.txt"]
    return Experiment("ACTPol", expParamFile, optParamFiles)

#Function that retuns the all V1 classes
def SOV1():
    #Locate parameter files
    expParamDir = "./experimentParams/SO_V1/"
    optParamDir = "./opticalParams/SO_V1/"

    #V1La
    expParamFile  = expParamDir+"V1La_expParams.txt"
    optParamFiles = [optParamDir+"V1La_150GHzOpticalParams.txt"]
    V1La = Experiment("V1La", expParamFile, optParamFiles)

    #V1La_2mirr
    expParamFile  = expParamDir+"V1La_2mirr_expParams.txt"
    optParamFiles = [optParamDir+"V1La_2mirr_150GHzOpticalParams.txt"]
    V1La_2mirr = Experiment("V1La_2mirr", expParamFile, optParamFiles)

    #V1Lb
    expParamFile  = expParamDir+"V1Lb_expParams.txt"
    optParamFiles = [optParamDir+"V1Lb_150GHzOpticalParams.txt"]
    V1Lb = Experiment("V1Lb", expParamFile, optParamFiles)

    #V1Ld
    expParamFile  = expParamDir+"V1Ld_expParams.txt"
    optParamFiles = [optParamDir+"V1Ld_150GHzOpticalParams.txt"]
    V1Ld = Experiment("V1Ld", expParamFile, optParamFiles)
    
    #V1Ld_2mirr
    expParamFile  = expParamDir+"V1Ld_2mirr_expParams.txt"
    optParamFiles = [optParamDir+"V1Ld_2mirr_150GHzOpticalParams.txt"]
    V1Ld_2mirr = Experiment("V1Ld_2mirr", expParamFile, optParamFiles)

    #V1p1L
    expParamFile  = expParamDir+"V1p1L_expParams.txt"
    optParamFiles = [optParamDir+"V1p1L_150GHzOpticalParams.txt"]
    V1p1L = Experiment("V1p1L", expParamFile, optParamFiles)    

    #V1p1L_4KApert
    expParamFile  = expParamDir+"V1p1L_expParams.txt"
    optParamFiles = [optParamDir+"V1p1L_4KApert_150GHzOpticalParams.txt"]
    V1p1L_4KApert = Experiment("V1p1L_4KApert", expParamFile, optParamFiles)    

    #V1p2L
    expParamFile  = expParamDir+"V1p2L_expParams.txt"
    optParamFiles = [optParamDir+"V1p2L_150GHzOpticalParams.txt"]
    V1p2L = Experiment("V1p2L", expParamFile, optParamFiles)

    return V1La, V1La_2mirr, V1Lb, V1Ld, V1Ld_2mirr, V1p1L, V1p1L_4KApert, V1p2L

#Class for handling experimental parameters
class Experiment:
    def __init__(self, experimentName, experimentalParamFile, opticalParamFileArr):
        #***** Private variables *****
        self.__mm     = 1.e-03 #m from mm
        self.__GHz    = 1.e+09 #GHz from Hz
        self.__aWrtHz = 1.e-18 #aW/rtHz from W/rtHz
        self.__pArtHz = 1.e-12 #pA/rtHz from A/rtHz
        self.__Hz     = 1.e-09 #Hz from GHz
        self.__pW     = 1.e-12 #pW from W

        #***** Public variables *****
        #Experiment name
        self.name = experimentName

        #Experimental parameters are drawn from the parameter files
        paramDict = self.__getExpParams(experimentalParamFile)
        #Psat/Popt factor
        self.psatFact = paramDict['psatFactor'][0]
        #Number of detector modes
        self.nModes = paramDict['numDetectorModes'][0]
        #Thermal carrier power index
        self.n = paramDict['thermalCarrierIndex'][0]
        #Bath Temperature [K]
        self.Tb = paramDict['bathTemp'][0]
        #Transition temperature [K]
        self.Tc = paramDict['criticalTemp'][0]
        #Noise equivalent current [aW/rtHz]
        self.nei = paramDict['noiseCurrent'][0]*self.__pArtHz
        #Bolometer operating resistance [Ohm]
        self.boloR = paramDict['boloResistance'][0]
        #Photon bunching factor
        self.bf = paramDict['photonBunchFactor'][0]

        #Band center [Hz]
        self.bandCenterArr = paramDict['bandCenter']*self.__GHz
        #Fractional bandwidth
        self.fbwArr = paramDict['percentBW']
        #Number of bands
        self.numBands = len(self.bandCenterArr)
        #Low frequency [Hz]
        self.loArr = self.bandCenterArr*(1. - 0.5*self.fbwArr)
        #High frequency [Hz]
        self.hiArr = self.bandCenterArr*(1. + 0.5*self.fbwArr)
        #Optical Parameters
        self.optParamFiles = opticalParamFileArr
        #Pixel size [m]
        self.pixSizeArr = paramDict['pixelSize']*self.__mm
        #Number of detectors
        self.nDetArr = paramDict['numDetectors']
        #Number of pixels
        self.nPixArr = self.nDetArr/2
        #Detector yield factor
        self.detYield = paramDict['detYield']

    #***** Private Functions *****
    #Function to read in parameter files into a dictionary
    def __getExpParams(self, file):
        with open(file, 'r') as doc:
            dict = {}
            for line in doc:
                if '*' in line:
                    continue
                if '#' in line:
                    continue
                if line.strip(): #Skip empty lines
                    key       = line.split()[0]
                    value     = np.array([float(x.strip('[],')) for x in line.split()[2:]])
                    dict[key] = value
        return dict

    #***** Public Functions *****
    #Function to get band optical parameters
    def getOpticalParams(self, bandNum):
        elemArr                 = np.loadtxt(self.optParamFiles[bandNum], dtype=np.str,   usecols=[0],     unpack=True, skiprows=1)
        emmArr, effArr, tempArr = np.loadtxt(self.optParamFiles[bandNum], dtype=np.float, usecols=[1,2,3], unpack=True, skiprows=1)
        return elemArr, emmArr, effArr, tempArr
