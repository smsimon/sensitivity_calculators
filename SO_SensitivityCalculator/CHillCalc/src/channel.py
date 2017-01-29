#!/usr/local/bin/python

#Class for handling CMB experiments

#python Version 2.7.2
import numpy as np
import physics as ph
import sky

#Class for handling a given frequency channel
class Channel:
    def __init__(self, channelDict, camera, opticalChain, atmFile=None):
        #***** Private variables *****
        self.__mm     = 1.e-03 #m from mm
        self.__GHz    = 1.e+09 #GHz from Hz
        self.__aWrtHz = 1.e-18 #aW/rtHz from W/rtHz
        self.__pArtHz = 1.e-12 #pA/rtHz from A/rtHz
        self.__Hz     = 1.e-09 #Hz from GHz
        self.__pW     = 1.e-12 #pW from W
        self.__camera       = camera
        self.__opticalChain = opticalChain
        self.__ph           = ph.Physics()
        self.__sky          = sky.Sky(atmFile)
        
        #***** Camera Parameters *****
        #Optical coupling to Focal Plane
        self.optCouple = self.__camera.opticalCouplingToFP
        #Detector F-number
        self.Fnumber = self.__camera.fnumber
        #Bath temperature
        self.Tb = self.__camera.Tb

        #***** Channel Parameters *****
        #Band ID
        self.bandID = channelDict['BandID']
        #Pixel ID
        self.pixelID = channelDict['PixelID']
        #Band Center
        self.bandCenter = self.__float(channelDict['BandCenter'], self.__GHz)
        #Fractional Bandwidth
        self.fbw = self.__float(channelDict['FBW'])
        #Pixel Size
        self.pixSize = self.__float(channelDict['PixSize'], self.__mm)
        #Number of detectors
        self.numDet = self.__float(channelDict['NumDet'])
        #Number of pixels
        self.numPix = self.numDet/2.
        #Waist factor
        self.wf = self.__float(channelDict['WaistFact'])
        #Detector efficiency
        self.detEff = self.__float(channelDict['DetEff'])
        #Psat
        self.psat = self.__float(channelDict['Psat'], self.__pW)
        #Psat Factor
        self.psatFact = self.__float(channelDict['PsatFact'])
        #Thermal Carrier Index
        self.n = self.__float(channelDict['CarrierIndex'])
        #Transition temperature
        self.Tc = self.__float(channelDict['TransTemp'])
        if self.Tc == 'NA':
            self.TcFrac = self.__float(channelDict['TcFrac'])
            self.Tc = self.Tb*self.TcFrac
        #Photon bunching factor
        self.bunchFact = self.__float(channelDict['BunchFactor'])
        #Detector yield
        self.detYield = self.__float(channelDict['Yield'])
        #Noise equivalent current
        self.nei = self.__float(channelDict['NEI'], self.__aWrtHz)
        #Number of modes
        self.nModes = self.__float(channelDict['nModes'])
        #Bolometer resistance
        self.boloR = self.__float(channelDict['boloR'])
        
        #Gemerate optical arrays
        self.genOptics()

    #***** Private Functions *****
    def __float(self, val, unit=1.0):
        try:
            return unit*float(val)
        except:
            return str(val)
        
    def __powFrac(self, T1, T2, f, fbw):
        return self.__ph.bbPower(1.0, f, fbw, T1)/self.__ph.bbPower(1.0, f, fbw, T2)
    
    def __getOptics(self):
        #Store name, emissivity, efficiency, and temperature
        elemArr = []
        emissArr = []
        effArr = []
        tempArr = []
        for opt in self.__opticalChain.opticArr:
            #Get element name
            elem = opt.element
            #Get element emissivity
            if opt.absorb != 'NA':
                if opt.absorbFreq != 'NA':
                    emiss = opt.absorb*(self.bandCenter/opt.absorbFreq)
                else:
                    emiss = opt.absorb
            else:
                if opt.element == 'Mirror':
                    emiss = 1. - self.__ph.ohmicEff(opt.conductivity, self.bandCenter)
                elif opt.element == 'Aperture':
                    emiss = 1. - self.__ph.spillEff(self.pixSize, self.Fnumber, self.wf, self.bandCenter)
                else:
                    emiss = self.__ph.dielectricLoss(opt.lossTan, opt.thick, opt.index, self.bandCenter)
            #Get element reflection
            if opt.refl != 'NA':
                refl = opt.refl
            else:
                if opt.element == 'Mirror':
                    refl = 1. - self.__ph.ruzeEff(opt.surfaceRough, self.bandCenter)
                elif opt.element == 'Aperture':
                    refl = 0.
                else:
                    refl = 0.
            #Get element scattering
            if opt.scattFrac == 'NA':
                scatt = 0.
            else:
                scatt = opt.scattFrac*refl
            #Get scattering temperature
            if opt.scattTemp == 'NA':
                scattTemp = self.Tb
            else:
                scattTemp = opt.scattTemp
            #Get temperature
            temp = opt.temp
            
            #Store parameters
            elemArr.append(elem)
            tempArr.append(temp)
            emissArr.append(emiss + scatt*self.__powFrac(scattTemp, temp, self.bandCenter, self.fbw))
            effArr.append(1. - refl - emiss)

        return elemArr, emissArr, effArr, tempArr

    #Function to read in parameter files into a dictionary
    def __getChParams(self, file):
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
    def genOptics(self):        
        #***** Sky Paramaeters *****
        skyElemArr, skyEmissArr, skyEffArr, skyTempArr = self.__sky.skyParams(self.bandCenter, self.fbw)

        #***** Optical Chain Parameters *****
        optElemArr, optEmissArr, optEffArr, optTempArr = self.__getOptics()

        #***** Detector Parameters *****
        detElemArr  = ['Detector']
        detEmissArr = [1. - self.detEff]
        detEffArr   = [self.detEff - (1. - self.optCouple)]
        detTempArr  = [self.Tb]
        
        #***** All Optical Parameters *****
        self.elemArr  = skyElemArr  + optElemArr  + detElemArr
        self.emissArr = skyEmissArr + optEmissArr + detEmissArr
        self.effArr   = skyEffArr   + optEffArr   + detEffArr
        self.tempArr  = skyTempArr  + optTempArr  + detTempArr
