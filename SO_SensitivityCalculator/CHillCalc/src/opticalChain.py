#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import optic as op

class OpticalChain:
    def __init__(self, opticalChainFile):
        #Read in the configuration file
        output = np.loadtxt(opticalChainFile, dtype=np.str)
        keyArr = output[0]
        elemArr = output[1:]
        #Create optic objects and store them into an array
        self.opticArr = []
        for elem in elemArr:
            dict = {}
            for i in range(len(keyArr)):
                dict[keyArr[i]] = elem[i]
            self.opticArr.append(op.Optic(dict))
