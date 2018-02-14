#python Version 2.7.2
import numpy       as np
import glob        as gb
import pickle      as pk
import foregrounds as fg
import units       as un
import os

class Sky:
    def __init__(self, log, nrealize=1, fgndDict=None, atmFile=None, pwv=None, generate=False, foregrounds=False):
        self.__log      = log
        self.__generate = generate
        self.__inclF    = foregrounds
        self.__fg       = fg.Foregrounds(fgndDict=fgndDict, nrealize=nrealize)
        self.__nfiles   = 10 #Number of files to break the atmDict.pkl file into

        self.atmFile   = atmFile
        self.pwv       = pwv
        self.medianPwv = 0.934 #Atacama
        self.maxPWV    = 8.0
        self.minPWV    = 0.0
        self.pklDir    = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/atmFiles/PKL/'
        self.txtDir    = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/atmFiles/TXT/'

        self.__initATM()
        self.__initATMDist()

    #***** Public methods ******
    def pwvSample(self):
        if self.pwv is not None: return self.pwv
        samp = np.random.choice(self.__pdfDict.keys(), size=1, p=self.__pdfDict.values()/np.sum(self.__pdfDict.values()))[0]
        if samp < self.minPWV:
            self.__log.log('Cannot have PWV %.1f < %.1f. Using %.1f instead' % (samp, self.minPWV, self.minPWV), 2)
            return self.minPWV
        elif samp > self.maxPWV:
            self.__log.log('Cannot have PWV %.1f > %.1f. Using %.1f instead' % (samp, self.maxPWV, self.maxPWV), 2)
            return self.maxPWV
        else:
            return samp
    def getPwv(self):
        return self.pwv
    def getMedianPwv(self):
        return self.medianPwv

    def atmSpectrum(self, pwv, elev, freqs):
        if self.atmFile:
            self.__log.log('Using provided ATM file -- ignoring provided PWV and El (%.1f, %.1f)' % (pwv, elev), 1)
            freq, temp, tran = np.loadtxt(self.atmFile, unpack=True, usecols=[0, 2, 3], dtype=np.float)
        else:
            freq, temp, tran = self.atmDict[(int(round(elev,0)), round(pwv,1))]
        freq = freq*un.GHzToHz; temp = np.interp(freqs, freq, temp); tran = np.interp(freqs, freq, tran)
        return freq.flatten().tolist(), temp.flatten().tolist(), tran.flatten().tolist()
    def synSpectrum(self, freqs):
        return self.__fg.syncSpecRad(1.0, freqs)
    def dstSpectrum(self, freqs):
        return self.__fg.dustSpecRad(1.0, freqs)
    def generate(self, pwv, elev, freqs):
        self.Ncmb = ['CMB' for f in freqs]; self.Tcmb = [2.725 for f in freqs]; self.Ecmb = [1. for f in freqs]; self.Acmb = [1. for f in freqs]
        self.Natm = ['ATM' for f in freqs]; freq, self.Tatm, self.Eatm = self.atmSpectrum(pwv, elev, freqs);     self.Aatm = [1. for f in freqs]
        if self.__inclF:
            self.Nsyn = ['SYNC' for f in freqs]; self.Tsyn = self.synSpectrum(freqs); self.Esyn = [1. for f in freqs]; self.Asyn = [1. for f in freqs]
            self.Ndst = ['DUST' for f in freqs]; self.Tdst = self.dstSpectrum(freqs); self.Edst = [1. for f in freqs]; self.Adst = [1. for f in freqs]
            return ([self.Ncmb, self.Nsyn, self.Ndst, self.Natm],
                    [self.Acmb, self.Asyn, self.Adst, self.Aatm],
                    [self.Ecmb, self.Esyn, self.Edst, self.Eatm],
                    [self.Tcmb, self.Tsyn, self.Tdst, self.Tatm])
        else:
            return ([self.Ncmb, self.Natm],
                    [self.Acmb, self.Aatm],
                    [self.Ecmb, self.Eatm],
                    [self.Tcmb, self.Tatm])

    #***** Private methods *****
    def __initATM(self):
        if self.__generate:
            atmFileArr                               = sorted(gb.glob(self.txtDir+"atm*.txt"))
            self.elevArr                             = np.array([float(atmFile.split('/')[-1].split('_')[1][:2])                                        for atmFile in atmFileArr])
            self.pwvArr                              = np.array([float(atmFile.split('/')[-1].split('_')[2][:4])*1e-3                                   for atmFile in atmFileArr])
            self.freqArr, self.tempArr, self.tranArr = np.hsplit(np.array([np.loadtxt(atmFile, usecols=[0, 2, 3], unpack=True)                          for atmFile in atmFileArr]), 3)
            self.atmDict                             = {(int(round(self.elevArr[i])), round(self.pwvArr[i],1)): (self.freqArr[i][0], self.tempArr[i][0], self.tranArr[i][0]) for i in range(len(atmFileArr))}
            for i in range(self.__nfiles):        
                sub_dict = self.atmDict.items()[i::self.__nfiles]
#                for k in self.atmDict.keys():
#                    sub_dict[k] = self.atmDict[k]
                pk.dump(sub_dict, open((self.pklDir +'atmDict_%d.pkl' % (i)), 'wb'))
        else:
            self.atmDict = {}
            for i in range(self.__nfiles):
                sub_dict = pk.load(open((self.pklDir+'atmDict_%d.pkl' % (i)), 'rb'))
                self.atmDict.update(sub_dict)

    def __initATMDist(self):
        self.__cdfDict    = pk.load(open(self.pklDir+'pwv_cdf.pkl'))
        self.__pdfDict    = {float(self.__cdfDict['pwv'][i]):       np.gradient(self.__cdfDict['cdf'],    np.diff(self.__cdfDict['pwv'])[0])[i]    for i in range(len(self.__cdfDict['pwv']   ))}

        self.__maxCdfDict = pk.load(open(self.pklDir+'pwvmax_pdf.pkl'))
        self.__maxPdfDict = {float(self.__maxCdfDict['pwvmax'][i]): np.gradient(self.__maxCdfDict['pdf'], np.diff(self.__maxCdfDict['pwvmax'])[0])[i] for i in range(len(self.__maxCdfDict['pwvmax']))}
