#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import glob as gb
import telescope as tp

class Experiment:
    def __init__(self, experimentDir, atmFile=None):
        #***** Private Variables *****
        self.__yrToSec = 365.25*24.*60.*60.
        #Retrieve experiment parameters
        params, vals = np.loadtxt(experimentDir+'/experiment.txt', unpack=True, usecols=[0,2], dtype=np.str)
        #Retrieve telescopes
        telescopeDirArr = sorted(gb.glob(experimentDir+'/*/'))

        #***** Public Variables *****
        self.tobs   = float(vals[params.tolist().index('ObservationTime')])*self.__yrToSec
        self.fsky   = float(vals[params.tolist().index('SkyFraction')])
        self.obsEff = float(vals[params.tolist().index('ObservationEfficiency')])
        self.netMgn = float(vals[params.tolist().index('NETmargin')])
        self.dir  = experimentDir
        self.name = experimentDir.rstrip('/').split('/')[-1]
        self.telescopes = []
        for telescopeDir in telescopeDirArr:
            self.telescopes.append(tp.Telescope(telescopeDir, atmFile))
