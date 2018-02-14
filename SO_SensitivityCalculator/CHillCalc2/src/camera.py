#python Version 2.7.2
import numpy        as np
import glob         as gb
import parameter    as pr
import opticalChain as oc
import channel      as ch

class Camera:
    def __init__(self, log, dir, sky, scn, nrealize=1, nobs=1, clcDet=1, specRes=1.e9):
        self.log = log
        self.sky = sky
        self.scn = scn

        self.dir        = dir
        self.configDir  = self.dir+'/config'
        self.bandDir    = self.configDir+'/Bands'
        self.name       = dir.rstrip('/').split('/')[-1]

        #Store the camera parameters
        paramArr, valArr = np.loadtxt(self.configDir+'/camera.txt', dtype=np.str, unpack=True, usecols=[0,2], delimiter='|')
        dict             = {paramArr[i].strip(): valArr[i].strip() for i in range(len(paramArr))}
        
        #Sample the camera paraemters
        def samp(param, pos=False, norm=False): 
            if nrealize == 1: return param.getAvg()
            else:             return param.sample(nsample=1, pos=pos, norm=norm)
        self.opticalCouplingToFP = samp(pr.Parameter(dict['Optical Coupling']), pos=True, norm=True)
        self.fnumber             = samp(pr.Parameter(dict['F Number'        ]), pos=True)
        self.Tb                  = samp(pr.Parameter(dict['Bath Temp'       ]), pos=True)

        #Collect band files
        def bandDict(dir):
            bandFiles = sorted(gb.glob(dir+'/*'))
            if len(bandFiles):
                nameArr = [nm.split('/')[-1].split('.')[0] for nm in bandFiles if "~" not in nm]
                if len(nameArr): return {nameArr[i]: bandFiles[i] for i in range(len(nameArr))}
                else:            return None
            else:
                return None

        #Store optical chain object
        self.optBandDict = bandDict(self.bandDir+'/Optics')
        self.optChain    = oc.OpticalChain(self.log, self.configDir+'/optics.txt', nrealize=nrealize, optBands=self.optBandDict)

        #Store channel objects
        self.detBandDict = bandDict(self.bandDir+'/Detectors')
        chans            = np.loadtxt(self.configDir+'/channels.txt', dtype=np.str, delimiter='|'); keyArr  = chans[0]; elemArr = chans[1:]
        self.chanDicts   = [{keyArr[i].strip(): elem[i].strip() for i in range(len(keyArr))} for elem in elemArr]
        self.channels    = [ch.Channel(log, chDict, self, self.optChain, self.sky, self.scn, detBandDict=self.detBandDict, nrealize=nrealize, nobs=nobs, clcDet=clcDet, specRes=specRes) for chDict in self.chanDicts]

        #Store pixel dictionary
        self.pixels   = {}
        for channel in self.channels:
            if channel.pixelID in self.pixels.keys(): self.pixels[channel.pixelID].append(channel)
            else:                                     self.pixels[channel.pixelID] = [channel]
