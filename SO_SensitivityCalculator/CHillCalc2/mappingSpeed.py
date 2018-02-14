#python Version 2.7.2
import numpy           as np
import glob            as gb
import multiprocessing as mp
import time            as tm
import sys             as sy

import experiment      as ex
import calculate       as cl
import display         as dp
import log             as lg

#Convert string to bool
def booll(str): 
    if 'True' in str or 'true' in str: return True
    else:                              return False

#Experiment Input Parameters
try:
    expIn = sy.argv[1]
except:
    print
    print 'Usage:   python mappingSpeed.py [Experiment Directory]'
    print 'Example: python mappingSpeed.py Experiments/SimonsObservatory/V3'
    print
    sy.exit(1)

#Simulation Input Parameters
params, vals = np.loadtxt('config/mappingSpeed_params.txt', unpack=True, skiprows=1, usecols=[0,1], dtype=np.str, delimiter='|')
inputDict = {params[i].strip(): vals[i].strip() for i in range(len(params))}
cores   = int(inputDict['Cores'])
verbose = int(inputDict['Verbosity'])
nrel    = int(inputDict['Experiments'])
nobs    = int(inputDict['Observations'])
clcDet  = int(inputDict['Detectors'])
oneElv  = str(inputDict['Elevation'])
if 'NA' in oneElv: oneElv = None
else:              oneElv = float(oneElv)
onePWV  = str(inputDict['PWV'])
if 'NA' in onePWV: onePWV = None
else:              onePWV = float(onePWV)
specRes = float(inputDict['Resolution'])*1.e9
fgnd    = booll(inputDict['Foregrounds'])
corr    = booll(inputDict['Correlations'])

#Logging
logFile = 'log/log_%d.txt' % (int(tm.time()))
logging = lg.Log(logFile, verbose)
logging.log('Logging to file "%s," printing with verbosity = %d' % (logFile, verbose), 2)

#Top-level methods for multiprocessing handling
def mp1(drr): return ex.Experiment(logging, drr, nrealize=nrel, nobs=nobs, clcDet=clcDet, elv=oneElv, pwv=onePWV, specRes=specRes, foregrounds=fgnd)
def mp2(exp): return cl.Calculate( logging, exp, corr)
def mp3(clc):
    chs = clc.chans; tps = clc.teles; shp = clc.shape
    senses = np.array([[[clc.calcSensitivity( chs[i][j][k], tps[i][j][k]) for k in range(shp[2])] for j in range(shp[1])] for i in range(shp[0])])
    optpow = np.array([[[clc.calcOpticalPower(chs[i][j][k], tps[i][j][k]) for k in range(shp[2])] for j in range(shp[1])] for i in range(shp[0])])
    clc.combineSensitivity( senses)
    clc.combineOpticalPower(optpow)
    return clc
def mp4(clcs): 
    dsp = dp.Display(logging, clcs)
    dsp.sensitivityTables()
    dsp.opticalPowerTables()

#Calculate mapping speed
#experiments = [mp1(expIn) for n   in range(nrel)]
#calculates  = [mp2(exp)   for exp in experiments]
#calculates  = [mp3(clc)   for clc in calculates ]
#mp4(calculates)

p = mp.Pool(cores)
designDirs = [expIn for n in range(nrel)]
experiments = p.map(mp1, designDirs)
calculates  = p.map(mp2, experiments)
calculates  = p.map(mp3, calculates)
mp4(calculates)
