#python Version 2.7.2
import numpy        as np
import observation  as ob
import scanStrategy as sc
import units        as un

class ObservationSet:
    def __init__(self, log, detArray, sky, scn, nobs=1):
        self.log      = log
        self.detArray = detArray
        self.sky      = sky
        self.scn      = scn

        #Store observation objects
        self.observations = [ob.Observation(self.log, self.detArray, self.sky, self.scn) for n in range(nobs)]
        
        #Store sky temperatures and efficiencies
        self.temps  = np.array([obs.temp  for obs in self.observations])
        self.effics = np.array([obs.effic for obs in self.observations])
