#python version 2.7.2
import numpy             as np
import physics           as ph
import units             as un
import matplotlib.pyplot as pt

class Display:
    def __init__(self, log, calcs):
        self.log     = log
        self.__calcs = calcs
        self.__ph    = ph.Physics() 
        self.exp     = self.__calcs[0].exp

        snsmeans = [calc.snsmeans for calc in calcs]
        snsstds  = [calc.snsstds  for calc in calcs]
        optmeans = [calc.optmeans for calc in calcs]
        optstds  = [calc.optstds  for calc in calcs]

        self.snsmeans = [[[(np.mean([snsmeans[m][i][j][k] for m in range(len(snsmeans))], axis=0)                                                                        ).tolist() for k in range(len(snsmeans[0][i][j]))] for j in range(len(snsmeans[0][i]))] for i in range(len(snsmeans[0]))]
        self.snsstds  = [[[(np.mean([snsstds[m][i][j][k]  for m in range(len(snsstds))],  axis=0) + np.std([snsmeans[m][i][j][k]  for m in range(len(snsmeans))], axis=0)).tolist() for k in range(len(snsstds[0][i][j]))]  for j in range(len(snsstds[0][i]))]  for i in range(len(snsstds[0] ))]
        self.optmeans = [[[(np.mean([optmeans[m][i][j][k] for m in range(len(optmeans))], axis=0)                                                                        ).tolist() for k in range(len(optmeans[0][i][j]))] for j in range(len(optmeans[0][i]))] for i in range(len(optmeans[0]))]
        self.optstds  = [[[(np.mean([optstds[m][i][j][k]  for m in range(len(optstds))],  axis=0) + np.std([optmeans[m][i][j][k]  for m in range(len(optmeans))], axis=0)).tolist() for k in range(len(optstds[0][i][j]))]  for j in range(len(optstds[0][i]))]  for i in range(len(optstds[0] ))]

        self.name   = []
        self.freq   = []; self.freqStd = []
        self.fbw    = []; self.fbwStd  = []
        self.numDet = []
        self.netArr = []; self.netArrStd = []
        self.sens   = []; self.sensStd   = []
        self.ms     = []; self.msStd     = []

        #Table column titles for camera files
        self.titleStrC  = str("%-5s | %-15s | %-15s | %-7s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-17s | %-15s | %-17s | %-15s\n" 
                              % ("Chan", "Frequency", "Frac Bandwidth", "Num Det", "Lyot Efficiency", "Optical Power", "Photon NEP", "Bolometer NEP", "Readout NEP", "Detector NEP", "Detector NET", "Array NET", "Mapping Speed", "Map Depth"))
        self.unitStrC   = str("%-5s | %-15s | %-15s | %-7s | %-15s | %-15s | %-15s | %-15s | %-15s | %-15s | %-17s | %-15s | %-17s | %-15s\n"
                              % ("", "[GHz]", "", "", "[%]", "[pW]", "[aW/rtHz]", "[aW/rtHz]", "[aW/rtHz]", "[aW/rtHz]", "[uK-rtSec]", "[uK-rtSec]", "[(uK^2 s)^-1]", "[uK-arcmin]"))
        self.breakStrC  = "-"*240+"\n"
        #Table column titles for telescope and experiment files
        self.titleStrTE = str("%-5s | %-15s | %-15s | %-7s | %-15s | %-17s | %-15s\n"
                              % ("Chan", "Frequency", "Frac Bandwidth", "Num Det", "Array NET", "Mapping Speed", "Map Depth"))
        self.unitStrTE  = str("%-5s | %-15s | %-15s | %-7s | %-15s | %-17s | %-15s\n"
                              % ("", "[GHz]", "", "", "[uK-rtSec]", "[(uK^2 s)^-1]", "[uK-arcmin]"))
        self.breakStrTE = "-"*110+"\n"

    #Generate sensitivity.txt files
    def sensitivityTables(self):
        #Full experiment
        experiment = self.exp
        fE = open(experiment.dir+'/sensitivity.txt', 'w')
        fE.write(self.titleStrTE)
        fE.write(self.breakStrTE)
        fE.write(self.unitStrTE)
        fE.write(self.breakStrTE)

        #Loop over telescopes
        for i in range(len(experiment.telescopes)):
            nameT   = []
            freqT   = []; freqStdT   = []
            fbwT    = []; fbwStdT    = []
            numDetT = []
            netArrT = []; netArrStdT = []
            sensT   = []; sensStdT   = []
            msT     = []; msStdT     = []

            telescope = experiment.telescopes[i]
            fT = open(telescope.dir+'/sensitivity.txt', "w")
            fT.write(self.titleStrTE)
            fT.write(self.breakStrTE)
            fT.write(self.unitStrTE)
            fT.write(self.breakStrTE)

            #Loop over cameras
            for j in range(len(telescope.cameras)):
                nameC   = []
                freqC   = []; freqStdC   = []
                fbwC    = []; fbwStdC    = []
                numDetC = []
                netArrC = []; netArrStdC = []
                sensC   = []; sensStdC   = []
                msC     = []; msStdC     = []

                camera = telescope.cameras[j]
                fC = open(camera.dir+'/sensitivity.txt', 'w')
                fC.write(self.titleStrC)
                fC.write(self.breakStrC)
                fC.write(self.unitStrC)
                fC.write(self.breakStrC)
                
                #Loop over channels
                for k in range(len(camera.channels)):
                    ch  = camera.channels[k]
                    ind = i*len(telescope.cameras) + j*len(camera.channels) + k
                    #Write channel values to camera file
                    printStr = str("%-5s | %-5.1f +/- %-5.1f | %-5.3f +/- %-5.3f | %-7d | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-6.1f +/- %-6.1f | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n"
                                   % (ch.name, 
                                      ch.bandCenter.getAvg()*un.HzToGHz,          ch.bandCenter.getStd()*un.HzToGHz,
                                      ch.fbw.getAvg(),                            ch.fbw.getStd(),
                                      ch.numDet,                                  
                                      self.snsmeans[i][j][k][0]*un.decToPct,      self.snsstds[i][j][k][0]*un.decToPct, 
                                      self.snsmeans[i][j][k][1]*un.WtoPw,         self.snsstds[i][j][k][1]*un.WtoPw, 
                                      self.snsmeans[i][j][k][2]*un.WrtHzToaWrtHz, self.snsstds[i][j][k][2]*un.WrtHzToaWrtHz,      
                                      self.snsmeans[i][j][k][3]*un.WrtHzToaWrtHz, self.snsstds[i][j][k][3]*un.WrtHzToaWrtHz,
                                      self.snsmeans[i][j][k][4]*un.WrtHzToaWrtHz, self.snsstds[i][j][k][4]*un.WrtHzToaWrtHz,
                                      self.snsmeans[i][j][k][5]*un.WrtHzToaWrtHz, self.snsstds[i][j][k][5]*un.WrtHzToaWrtHz,
                                      self.snsmeans[i][j][k][6]*un.KTouK,         self.snsstds[i][j][k][6]*un.KTouK,
                                      self.snsmeans[i][j][k][7]*un.KTouK,         self.snsstds[i][j][k][7]*un.KTouK,
                                      self.snsmeans[i][j][k][8]*un.uK2ToK2,       self.snsstds[i][j][k][8]*un.uK2ToK2,
                                      self.snsmeans[i][j][k][9]*un.KTouK,         self.snsstds[i][j][k][9]*un.KTouK))
                    fC.write(printStr)
                    fC.write(self.breakStrC)

                    #Store channel values in camera arrays
                    nameC.append(ch.name)
                    freqC.append(ch.bandCenter.getAvg());         freqStdC.append(ch.bandCenter.getStd())
                    fbwC.append(ch.fbw.getAvg());                 fbwStdC.append(ch.fbw.getStd())
                    numDetC.append(ch.numDet)
                    netArrC.append(   self.snsmeans[i][j][k][7]); netArrStdC.append(self.snsstds[i][j][k][7])
                    msC.append(       self.snsmeans[i][j][k][8]); msStdC.append(    self.snsstds[i][j][k][8])
                    sensC.append(     self.snsmeans[i][j][k][9]); sensStdC.append(  self.snsstds[i][j][k][9])

                #Write cumulative sensitivity for camera
                printStr = str("%-5s | %-33s | %-7d | %-125s | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n" 
                               % ('Total', '', sum(numDetC), '', 
                                  self.__ph.invVar(netArrC)*un.KTouK, self.__ph.invVar(netArrStdC)*un.KTouK,
                                  sum(msC)*un.uK2ToK2,                sum(msStdC)*un.uK2ToK2,
                                  self.__ph.invVar(sensC)*un.KTouK,   self.__ph.invVar(sensStdC)*un.KTouK))
                fC.write(printStr)
                fC.close()
                
                #Store camera parameters in telescope arrays
                nameT.append(  nameC)
                freqT.append(  freqC);   freqStdT.append(  freqStdC)
                fbwT.append(   fbwC);    fbwStdT.append(   fbwStdC)
                numDetT.append(numDetC)
                netArrT.append(netArrC); netArrStdT.append(netArrStdC)
                msT.append(    msC);     msStdT.append(    msStdC    )
                sensT.append(  sensC);   sensStdT.append(  sensStdC  )

            #Combine all cameras in telescope
            inds = np.argsort(np.array(freqT).flatten())
            nameT   = np.array(nameT).flatten()[inds]
            freqT   = np.array(freqT).flatten()[inds];   freqStdT = np.array(freqStdT).flatten()[inds]
            fbwT    = np.array(fbwT).flatten()[inds];    fbwStdT  = np.array(fbwStdT).flatten()[inds]
            numDetT = np.array(numDetT).flatten()[inds]
            netArrT = np.array(netArrT).flatten()[inds]; netArrStdT = np.array(netArrStdT).flatten()[inds]
            msT     = np.array(msT).flatten()[inds];     msStdT     = np.array(msStdT).flatten()[inds]
            sensT   = np.array(sensT).flatten()[inds];   sensStdT   = np.array(sensStdT).flatten()[inds]

            #Combine repeat channels in this telescope
            for m in range(len(nameT)):
                if m >= len(nameT): continue
                for n in range(m, len(nameT)):
                    if m == n or n >= len(nameT):
                        continue
                    if nameT[m] == nameT[n]:
                        freqT[m]       = np.mean([freqT[m], freqT[n]])
                        freqStdT[m]    = np.std([freqT[m], freqT[n]]) + np.mean([freqStdT[m], freqStdT[n]])
                        fbwT[m]        = np.mean([fbwT[m], fbwT[n]])
                        fbwStdT[m]     = np.std([fbwT[m], fbwT[n]]) + np.mean([fbwStdT[m], fbwStdT[n]])
                        numDetT[m]    += numDetT[n]

                        netArrTv    = self.__ph.invVar([netArrT[m],    netArrT[n]])
                        netArrStdTv = np.mean([netArrStdT[m], netArrStdT[n]])
                        sensTv      = self.__ph.invVar([sensT[m],      sensT[n]])
                        sensStdTv   = np.mean([sensStdT[m],   sensStdT[n]])
                        msTv        = 1./np.power(netArrTv,   2.)
                        msStdTv     = np.mean([msStdT[m]*(msT/msT[m]) + msStdT[n]*(msT/msT[n])])
                        
                        netArrT[m]    = netArrTv
                        netArrStdT[m] = netArrStdTv
                        sensT[m]      = sensTv
                        sensStdT[m]   = sensStdTv
                        msT[m]        = msTv
                        msStdT[m]     = msStdTv
                        
                        nameT      = np.delete(nameT,      n)
                        freqT      = np.delete(freqT,      n)
                        freqStdT   = np.delete(freqStdT,   n)
                        fbwT       = np.delete(fbwT,       n)
                        fbwStdT    = np.delete(fbwStdT,    n)
                        numDetT    = np.delete(numDetT,    n)
                        netArrT    = np.delete(netArrT,    n)
                        netArrStdT = np.delete(netArrStdT, n)
                        sensT      = np.delete(sensT,      n)
                        sensStdT   = np.delete(sensStdT,   n)
                        msT        = np.delete(msT,        n)
                        msStdT     = np.delete(msStdT,     n)

                #Write combined telescope sensitivities for each channel
                printStr = ("%-5s | %-5.1f +/- %-5.1f | %-5.3f +/- %-5.3f | %-7d | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n" 
                            % (nameT[m],
                               freqT[m]*un.HzToGHz, freqStdT[m]*un.HzToGHz,
                               fbwT[m],             fbwStdT[m],
                               numDetT[m],
                               netArrT[m]*un.KTouK, netArrStdT[m]*un.KTouK,
                               msT[m]*un.uK2ToK2,   msStdT[m]*un.uK2ToK2,
                               sensT[m]*un.KTouK,   sensStdT[m]*un.KTouK))
                fT.write(printStr)
                fT.write(self.breakStrTE)
                
            #Store telescope sensitivities in experiment arrays
            self.name.append(nameT)
            self.freq.append(freqT);     self.freqStd.append(freqStdT)
            self.fbw.append(fbwT);       self.fbwStd.append(fbwStdT)
            self.numDet.append(numDetT)
            self.netArr.append(netArrT); self.netArrStd.append(netArrStdT)
            self.ms.append(msT);         self.msStd.append(msStdT)
            self.sens.append(sensT);     self.sensStd.append(sensStdT)
        
            #Print the total sensitivity for the telescopes
            printStr = ("%-5s | %-33s | %-7d | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n" 
                        % ('Total', '', sum(numDetT), 
                           self.__ph.invVar(netArrT)*un.KTouK, self.__ph.invVar(netArrStdT)*un.KTouK,
                           sum(msT)*un.uK2ToK2,                sum(msStdT)*un.uK2ToK2,
                           self.__ph.invVar(sensT)*un.KTouK,   self.__ph.invVar(sensStdT)*un.KTouK))
            fT.write(printStr)
            fT.close()

        #Combine all telescopes in experiment
        inds = np.argsort(np.array(self.freq).flatten())
        self.name   = np.array(self.name).flatten()[inds]
        self.freq   = np.array(self.freq).flatten()[inds];   self.freqStd = np.array(self.freqStd).flatten()[inds]
        self.fbw    = np.array(self.fbw).flatten()[inds];    self.fbwStd  = np.array(self.fbwStd).flatten()[inds]
        self.numDet = np.array(self.numDet).flatten()[inds]
        self.netArr = np.array(self.netArr).flatten()[inds]; self.netArrStd = np.array(self.netArrStd).flatten()[inds]
        self.ms     = np.array(self.ms).flatten()[inds];     self.msStd     = np.array(self.msStd).flatten()[inds]
        self.sens   = np.array(self.sens).flatten()[inds];   self.sensStd   = np.array(self.sensStd).flatten()[inds]

        #Combine repeat frequencies in this experiment
        for m in range(len(self.name)):
            if m >= len(self.name): continue
            for n in range(m, len(self.name)):
                if m == n or n >= len(self.name):
                    continue
                if self.name[m] == self.name[n]:
                    self.freq[m]      = np.mean([self.freq[m], self.freq[n]])
                    self.freqStd[m]   = np.std([self.freq[m], self.freq[n]]) + np.mean([self.freqStd[m], self.freqStd[n]])
                    self.fbw[m]       = np.mean([self.fbw[m], self.fbw[n]])
                    self.fbwStd[m]    = np.std([self.fbw[m], self.fbw[n]]) + np.mean([self.fbwStd[m], self.fbwStd[n]])
                    self.numDet[m]    += self.numDet[n]
                    
                    netArr    = self.__ph.invVar([self.netArr[m],    self.netArr[n]])
                    netArrStd = np.mean([self.netArrStd[m], self.netArrStd[n]])
                    sens      = self.__ph.invVar([self.sens[m],      self.sens[n]])
                    sensStd   = np.mean([self.sensStd[m],   self.sensStd[n]])
                    ms        = 1./np.power(netArr,   2.)
                    msStd     = np.mean([self.msStd[m]*(ms/self.ms[m]) + self.msStd[n]*(ms/self.ms[n])])

                    self.netArr[m]     = netArr
                    self.netArrStd[m]  = netArrStd
                    self.sens[m]       = sens
                    self.sensStd[m]    = sensStd
                    self.ms[m]         = ms
                    self.msStd[m]      = msStd
                    
                    self.name      = np.delete(self.name,      n)
                    self.freq      = np.delete(self.freq,      n)
                    self.freqStd   = np.delete(self.freqStd,   n)
                    self.fbw       = np.delete(self.fbw,       n)
                    self.fbwStd    = np.delete(self.fbwStd,    n)
                    self.numDet    = np.delete(self.numDet,    n)
                    self.netArr    = np.delete(self.netArr,    n)
                    self.netArrStd = np.delete(self.netArrStd, n)
                    self.sens      = np.delete(self.sens,      n)
                    self.sensStd   = np.delete(self.sensStd,   n)
                    self.ms        = np.delete(self.ms,        n)
                    self.msStd     = np.delete(self.msStd,     n)

            #Write combined experiment sensitivities for each channel
            printStr = ("%-5s | %-5.1f +/- %-5.1f | %-5.3f +/- %-5.3f | %-7d | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n" 
                        % (self.name[m],
                           self.freq[m]*un.HzToGHz, self.freqStd[m]*un.HzToGHz,
                           self.fbw[m],             self.fbwStd[m],
                           self.numDet[m],
                           self.netArr[m]*un.KTouK, self.netArrStd[m]*un.KTouK,
                           self.ms[m]*un.uK2ToK2,   self.msStd[m]*un.uK2ToK2,
                           self.sens[m]*un.KTouK,   self.sensStd[m]*un.KTouK))
            fE.write(printStr)
            fE.write(self.breakStrTE)
        
        #Print the total sensitivity for the telescopes
        printStr = ("%-5s | %-33s | %-7d | %-5.2f +/- %-5.2f | %-6.4f +/- %-6.4f | %-5.1f +/- %-5.1f\n" 
                    % ('Total', '', sum(self.numDet), 
                       self.__ph.invVar(self.netArr)*un.KTouK, self.__ph.invVar(self.netArrStd)*un.KTouK,
                       sum(self.ms)*un.uK2ToK2,                sum(self.msStd)*un.uK2ToK2,
                       self.__ph.invVar(self.sens)*un.KTouK,   self.__ph.invVar(self.sensStd)*un.KTouK))
        fE.write(printStr)
        fE.close()        

        return
    
    #Generate opticalPower.txt files
    def opticalPowerTables(self):
        title     = "| %-15s | %-15s | %-15s | %-15s |\n" % ("Element", "Power from Sky", "Power to Detect", "Cumulative Eff")
        units     = "| %-15s | %-15s | %-15s | %-15s |\n" % ("",        "[pW]",           "[pW]",            ""              )      
        row       = ("-"*73)+"\n"
        for i in range(len(self.exp.telescopes)):
            telescope = self.exp.telescopes[i]
            for j in range(len(telescope.cameras)):
                camera = telescope.cameras[j]
                fi = open(camera.dir+'/opticalPower.txt', 'w')
                for k in range(len(camera.channels)):
                    #ind = i*len(telescope.cameras) + j*len(camera.channels) + k
                    ch = camera.channels[k]
                    bandName = ch.bandID
                    bandTitle = ("*"*24)+(" %11s %-12s " % (camera.name, bandName))+("*"*23)+"\n"
                    fi.write(bandTitle)
                    fi.write(row)
                    fi.write(title)
                    fi.write(row)
                    fi.write(units)
                    fi.write(row)
                    for m in range(len(ch.elem[0][0])):
                        elemName = ch.elem[0][0][m]
                        values = ("| %-15s | %-5.2f +/- %-5.2f | %-5.2f +/- %-5.2f | %-5.3f +/- %-5.3f |\n" 
                                  % (elemName, 
                                     self.optmeans[i][j][k][0][m]*un.WtoPw, self.optstds[i][j][k][0][m]*un.WtoPw, 
                                     self.optmeans[i][j][k][1][m]*un.WtoPw, self.optstds[i][j][k][1][m]*un.WtoPw, 
                                     self.optmeans[i][j][k][2][m],          self.optstds[i][j][k][2][m]))
                        fi.write(values)
                        fi.write(row)
                    fi.write("\n\n")
                fi.close()
