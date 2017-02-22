#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np

class Optic:
    def __init__(self, opticDict):
        #***** Private Variables *****
        self.__mm  = 1.e-03
        self.__Spm = 1.e+06
        self.__um  = 1.e-06
        self.__GHz = 1.e+09
        
        #***** Public Variables *****
        #Element name
        self.element = self.__float(opticDict['Element'])
        #Temperature
        self.temp = self.__float(opticDict['Temp'])
        #Thickness
        self.thick = self.__float(opticDict['Thick'], self.__mm)
        #Index
        self.index = self.__float(opticDict['Index'])
        #Loss Tangent
        self.lossTan = self.__float(opticDict['LossTan'], 1.e-4)
        #Conductivity
        self.conductivity = self.__float(opticDict['Conductivity'], self.__Spm)
        #Absorption
        self.absorb = self.__float(opticDict['Absorb'])
        #Absorption frequency
        self.absorbFreq = self.__float(opticDict['AbsorbFreq'], self.__GHz)
        #Spillover
        self.spill = self.__float(opticDict['Spill'])
        #Temperature that the spillover lands on
        self.spillTemp = self.__float(opticDict['SpillTemp'])
        #Surface Roughness
        self.surfaceRough = self.__float(opticDict['SurfaceRough'], self.__um)
        #Reflection
        self.refl = self.__float(opticDict['Refl'])
        #Scattering Fraction
        self.scattFrac = self.__float(opticDict['ScattFrac'])
        #Scattering Temperature 
        self.scattTemp = self.__float(opticDict['ScattTemp'])
        
    #***** Private Functions *****
    def __float(self, val, unit=1.0):
        try:
            return unit*float(val)
        except:
            return str(val)
