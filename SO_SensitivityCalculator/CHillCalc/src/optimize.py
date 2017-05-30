#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import calculate as calc
import matplotlib.pyplot as plt
import physics as ph

class Optimize:
    def __init__(self, exp):
        #***** Private Variables *****
        self.__mmToM = 1.e-03
        self.__mToMm = 1.e+03
        self.__GHz   = 1.e-09
        self.__uK2   = 1.e-12
        self.__exp   = exp
        self.__clc   = calc.Calculate(self.__exp)
        self.__ph    = ph.Physics()
        #Set plotting parameters
        plt.rc('font', size=32)
        plt.rc('font', family='serif')
        self.__lw = 3
        
    #***** Public Methods *****
    def optimizeFP(self, plotInMM=False):
        pixSizesFnum = np.arange(0.000001, 3.050001, 0.05)
        #Merge pixel dictionaries from all telescopes
        self.pixels = {}
        for t in self.__exp.telescopes: 
            self.pixels = dict(self.pixels.items() + t.pixels.items())
        figNum = 0
        #Calculate mapping speed for various pixels
        for pix in self.pixels:
            plt.figure(figsize=(15,12))
            msArrArr = []
            corrmsArrArr = []
            chans = self.pixels[pix]
            freqStr = ''
            #Pixel sizes
            if plotInMM: 
                pixLo = pixSizesFnum[0]*chans[-1].Fnumber*self.__ph.lamb(chans[-1].bandCenter)
                pixHi = pixSizesFnum[-1]*chans[0].Fnumber*self.__ph.lamb(chans[0].bandCenter )
                pixSp = 0.0003 #m
                pixSizes = np.arange(pixLo, pixHi, pixSp) #m
            for ch in chans:
                freqStr += '%d_' % (int(ch.bandCenter*1.e-9))
                if not plotInMM: 
                    pixSizes = pixSizesFnum*ch.Fnumber*self.__ph.lamb(ch.bandCenter) #m
                msArr = []
                corrmsArr = []
                origSize   = ch.pixSize
                origDetNum = ch.numDet
                yld        = ch.detYield
                for size in pixSizes:
                    ch.pixSize = size
                    ch.numDet  = origDetNum*(origSize/size)**2
                    ch.genOptics()
                    out1 = self.__clc.calcMappingSpeed(ch)
                    out2 = self.__clc.calcMappingSpeed(ch,corr=True)
                    msArr.append(    out1[12])
                    corrmsArr.append(out2[12])
                msArrArr.append(    np.array(msArr    ))
                corrmsArrArr.append(np.array(corrmsArr))
                if not plotInMM:
                    p1 = plt.plot(pixSizesFnum, np.array(msArr)*self.__uK2,     linewidth=self.__lw, label='%.1f GHz' % (ch.bandCenter*self.__GHz))
                    p2 = plt.plot(pixSizesFnum, np.array(corrmsArr)*self.__uK2, linewidth=self.__lw, color=p1[0].get_color(), linestyle='--')
                else:
                    p1 = plt.plot(pixSizes*self.__mToMm,     np.array(msArr)*self.__uK2,     linewidth=self.__lw, label='%.1f GHz' % (ch.bandCenter*self.__GHz))
                    p2 = plt.plot(pixSizes*self.__mToMm,     np.array(corrmsArr)*self.__uK2, linewidth=self.__lw, color=p1[0].get_color(), linestyle='--')
            #Plot combined mapping speed if plotting in mm
            if plotInMM:
                yArr     = np.sum(msArrArr,axis=0)
                corryArr = np.sum(corrmsArrArr,axis=0)
                p1 = plt.plot(pixSizes*self.__mToMm,     yArr*self.__uK2,     linewidth=self.__lw, label='Combined')
                p2 = plt.plot(pixSizes*self.__mToMm,     corryArr*self.__uK2, linewidth=self.__lw, color=p1[0].get_color(), linestyle='--')
            #Plot phantom lines for legend
            if not plotInMM:
                plt.plot(pixSizesFnum, [-1. for x in pixSizesFnum], color='k', linestyle='-', label='Uncorr', linewidth=self.__lw)
                plt.plot(pixSizesFnum, [-1. for x in pixSizesFnum], color='k', linestyle='--', label='Corr', linewidth=self.__lw)
            else:
                plt.plot(pixSizes*self.__mToMm,     [-1. for x in pixSizes],     color='k', linestyle='-', label='Uncorr', linewidth=self.__lw)
                plt.plot(pixSizes*self.__mToMm,     [-1. for x in pixSizes],     color='k', linestyle='--', label='Corr', linewidth=self.__lw)
            #plt.ylim([0., np.amax(yArr*self.__uK2)*(1+0.1)])
            plt.title('%s, Pixel %s, F/# = %.1f' % (self.__exp.name, pix, ch.Fnumber))
            if not plotInMM: 
                plt.xlabel('Pixel Size [F-lambda]')
                plt.xlim([0., np.amax(pixSizesFnum)])
                plt.ylim([0., np.amax(np.array(msArrArr)*self.__uK2)*(1+0.1)])
            else:            
                plt.xlabel('Pixel Size [mm]')
                plt.xlim([0., np.amax(pixSizes*self.__mToMm)])
                plt.ylim([0., np.amax(np.sum(msArrArr,axis=0)*self.__uK2)*(1+0.1)])
            #plt.ylabel('Normalized Mapping Speed')
            plt.ylabel('Mapping Speed [(uK^2 s)^-1]')
            plt.legend(loc='best', fontsize=24)
            plt.savefig('%s/Pixel_%d_%soptimize.jpg' % (self.__exp.dir, int(pix), freqStr))
            figNum += 1
            #Save data to text file
            if not plotInMM: np.savetxt('%s/Pixel_%d_%soptimize.txt' % (self.__exp.dir, int(pix), freqStr), np.array([pixSizesFnum.tolist()] + (np.array(msArrArr)*self.__uK2).tolist() + (np.array(corrmsArrArr)*self.__uK2).tolist()).T, fmt='%-10.5f', header='DetSpace [F-lamb],  MS w/o Corr [uK^-2 s^-1],  MS w/ Corr [uK^-2 s^-1]')
            else:            np.savetxt('%s/Pixel_%d_%soptimize.txt' % (self.__exp.dir, int(pix), freqStr), np.array([pixSizes.tolist()]     + (np.array(msArrArr)*self.__uK2).tolist() + (np.array(corrmsArrArr)*self.__uK2).tolist()).T, fmt='%-10.5f', header='DetSpace [mm],      MS w/o Corr [uK^-2 s^-1],  MS w/ Corr [uK^-2 s^-1]')

