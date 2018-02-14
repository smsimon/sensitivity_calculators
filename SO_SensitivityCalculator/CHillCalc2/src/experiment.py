#python Version 2.7.2
import numpy     as np
import glob      as gb
import telescope as tp

class Experiment:
    def __init__(self, log, dir, nrealize=1, nobs=1, clcDet=1, elv=None, pwv=None, specRes=1.e9, foregrounds=False):
        self.log       = log        
        self.dir       = dir
        self.configDir = self.dir+'/config'
        self.name      = self.dir.rstrip('/').split('/')[-1]

        #Store foreground parameters
        try:
            params, vals = np.loadtxt(self.configDir+'/foregrounds.txt', unpack=True, usecols=[0,2], dtype=np.str, delimiter='|')
            fgndDict     = {params[i].strip(): vals[i].strip() for i in range(len(params))}
            if foregrounds: self.log.log("Using foreground parameters in %s"    % (self.configDir+'/foregrounds.txt'), 1)
            else:           self.log.log("Ignoring foreground parameters in %s" % (self.configDir+'/foregrounds.txt'), 1)
        except:
            fgndDict = None
        
        #Store telescope objects
        telescopeDirs   = sorted(gb.glob(dir+'/*/')); telescopeDirs = [x for x in telescopeDirs if 'config' not in x]
        self.telescopes = [tp.Telescope(self.log, dir, fgndDict=fgndDict, nrealize=nrealize, nobs=nobs, clcDet=clcDet, elv=elv, pwv=pwv, specRes=specRes, foregrounds=foregrounds) for dir in telescopeDirs]
