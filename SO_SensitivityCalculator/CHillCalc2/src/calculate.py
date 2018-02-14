#using Python 2.7.2
import numpy       as np
import sensitivity as sn

class Calculate:
    def __init__(self, log, exp, corr=True):
        self.log   = log
        self.exp   = exp
        
        self.chans = [[[ch for ch in camera.channels] for camera in telescope.cameras] for telescope in self.exp.telescopes]
        self.cams  = [[[cm for i  in camera.channels] for cm     in telescope.cameras] for telescope in self.exp.telescopes]
        self.teles = [[[tp for i  in camera.channels] for ii     in telescope.cameras] for tp        in self.exp.telescopes]
        self.sens  = sn.Sensitivity(log, exp, corr)
        self.shape = np.shape(self.chans)

    #***** Public Methods *****
    #Calculate sensitivity for this channel
    def calcSensitivity(self, ch, tp):
        return self.sens.sensitivity(ch, tp)
    
    #Calculate optical power for this channel
    def calcOpticalPower(self, ch, tp):
        return self.sens.opticalPower(ch, tp)

    #Combine the sensitivities of multiple channels
    def combineSensitivity(self, sensArr):
        self.snsmeans = [[[[sensArr[i][j][k][0][m] for m in range(len(sensArr[i][j][k][0]))] for k in range(len(sensArr[i][j]))] for j in range(len(sensArr[i]))] for i in range(len(sensArr))]
        self.snsstds  = [[[[sensArr[i][j][k][1][m] for m in range(len(sensArr[i][j][k][1]))] for k in range(len(sensArr[i][j]))] for j in range(len(sensArr[i]))] for i in range(len(sensArr))]

    #Combine the optical powers of multiple channels
    def combineOpticalPower(self, optArr):
        self.optmeans = [[[[optArr[i][j][k][0][m]  for m in range(len(optArr[i][j][k][0]))]  for k in range(len(optArr[i][j]))]  for j in range(len(optArr[i]))]  for i in range(len(optArr))]
        self.optstds  = [[[[optArr[i][j][k][1][m]  for m in range(len(optArr[i][j][k][1]))]  for k in range(len(optArr[i][j]))]  for j in range(len(optArr[i]))]  for i in range(len(optArr))]
        #self.optmeans = np.array([[optArr[i][0][j]  for j in range(len(optArr[i][0]))]  for i in range(len(optArr))] )
        #self.optstds  = np.array([[optArr[i][1][j]  for j in range(len(optArr[i][1]))]  for i in range(len(optArr))] )
        #self.optmeans = np.array([[[optArr[i][0][j][k]  for k in range(len(optArr[i][0][j]))] for j in range(len(optArr[i][0]))]  for i in range(len(optArr))] )
        #self.optstds  = np.array([[[optArr[i][1][j][k]  for k in range(len(optArr[i][1][j]))] for j in range(len(optArr[i][1]))]  for i in range(len(optArr))] )
        #self.optmeans = np.reshape(self.optmeans, (len(self.optmeans), len(self.optmeans[0]), len(self.optmeans[0][0])))
        #self.optstds  = np.reshape(self.optstds,  (len(self.optstds),  len(self.optstds[0]),  len(self.optstds[0][0])))
