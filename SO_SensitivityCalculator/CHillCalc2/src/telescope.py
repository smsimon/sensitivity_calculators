#python Version 2.7.2
import numpy        as np
import parameter    as pr
import camera       as cm
import glob         as gb
import units        as un
import sky          as sk
import scanStrategy as sc

class Telescope:
    def __init__(self, log, dir, fgndDict=None, nrealize=1, nobs=1, clcDet=1, elv=None, pwv=None, specRes=1.e9, foregrounds=False):
        self.log        = log
        self.dir        = dir
        self.configDir  = dir+'config/'
        self.name       = dir.rstrip('/').split('/')[-1]

        #Store the program parameters
        params, vals    = np.loadtxt(self.configDir+'program.txt', unpack=True, usecols=[0,2], dtype=np.str, delimiter='|')
        dict            = {params[i].strip(): vals[i].strip() for i in range(len(params))}
        self.log.log('Using program parameter file %s' % (self.configDir+'program.txt'), 1)
        
        #Sample the program parameters
        def samp(param, pos=False, norm=False): 
            if nrealize == 1: return param.getAvg()
            else:             return param.sample(nsample=1, pos=pos, norm=norm)
        self.tobs       = samp(pr.Parameter(dict['Observation Time'], un.yrToSec), pos=True)
        self.fsky       = samp(pr.Parameter(dict['Sky Fraction']),                 pos=True, norm=True)
        self.obsEff     = samp(pr.Parameter(dict['Observation Efficiency']),       pos=True, norm=True)
        self.netMgn     = samp(pr.Parameter(dict['NET Margin']),                   pos=True)

        #Store sky object
        atmFile = sorted(gb.glob(self.configDir+'/atm*.txt'))
        if len(atmFile) == 0:
            atmFile = None
            self.log.log("No custom atmosphere provided; using Atacama MERRA AM-simulated sky", 1)
        elif len(atmFile) > 1:
            atmFile = None
            self.log.log('More than one atm file found in %s; ignoring them all' % (self.configDir), 2)
        else:
            atmFile = atmFile[0]
            self.log.log("Using custom atmosphere defined in %s" % (atmFile), 2)
        self.sky = sk.Sky(self.log, nrealize=1, fgndDict=fgndDict, atmFile=atmFile, pwv=pwv, generate=False, foregrounds=foregrounds)

        #Store scan strategy object
        scanFile = sorted(gb.glob(self.configDir+'/elevation.txt'))
        if len(scanFile) == 0:
            scanDict = None
            self.log.log("No scan strategy provided; using default elevation distribution", 1)
        elif len(scanFile) > 1:
            scanDict = None
            self.log.log('More than one scan strategy file found in %s; ignoring them all' % (self.configDir), 2)
        else:
            scanFile = scanFile[0]
            params, vals    = np.loadtxt(scanFile, unpack=True, usecols=[0,1], dtype=np.str, delimiter='|')
            scanDict        = {params[i].strip(): vals[i].strip() for i in range(2, len(params))}
            self.log.log("Using scan strategy defined in %s" % (scanFile), 2)
        self.scn = sc.ScanStrategy(self.log, scanDict=scanDict, elv=elv)

        #Store camera objects
        cameraDirs   = sorted(gb.glob(dir+'/*/')); cameraDirs = [x for x in cameraDirs if 'config' not in x]
        self.cameras = [cm.Camera(self.log, dir, self.sky, self.scn, nrealize=nrealize, nobs=nobs, clcDet=clcDet, specRes=specRes) for dir in cameraDirs]
