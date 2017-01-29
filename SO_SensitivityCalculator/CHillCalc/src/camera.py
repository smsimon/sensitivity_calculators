#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np

class Camera:
    def __init__(self, cameraFile):
        #Unpack the config file
        paramArr, valArr = np.loadtxt(cameraFile, dtype=np.str, unpack=True, usecols=[0,2])
        dict = {}
        for i in range(len(paramArr)):
            dict[paramArr[i]] = valArr[i]

        # ***** Public Variables *****
        self.opticalCouplingToFP = self.__float(dict['OpticalCouplingToFP'])
        self.fnumber = self.__float(dict['Fnumber'])
        self.Tb = self.__float(dict['BathTemp'])
        
    #***** Private functions *****
    def __float(self, val):
        try:
            return float(val)
        except:
            return str(val)

