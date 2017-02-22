#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import calculate as calc
import matplotlib.pyplot as plt

class Optimize:
    def __init__(self, exp):
        #***** Private Variables *****
        self.__mmToM = 1.e-03
        self.__mToMm = 1.e+03
        self.__GHz   = 1.e-09
        self.__uK2   = 1.e-12
        self.__exp   = exp
        self.__clc   = calc.Calculate(self.__exp)
        #Set plotting parameters
        plt.rc('font', size=32)
        plt.rc('font', family='serif')
        self.__lw = 3
        
    #***** Public Methods *****
    def optimizeFP(self):
        #Pixel sizes to be considered
        pixSizes = np.arange(0.5, 10.0, .2)*self.__mmToM
        #Merge pixel dictionaries from all telescopes
        self.pixels = {}
        for t in self.__exp.telescopes: 
            self.pixels = dict(self.pixels.items() + t.pixels.items())
        figNum = 0
        #Calculate mapping speed for various pixels
        for pix in self.pixels:
            plt.figure(figsize=(15,12))
            msArrArr = []
            chans = self.pixels[pix]
            for ch in chans:
                msArr = []
                origSize   = ch.pixSize
                origDetNum = ch.numDet
                for size in pixSizes:
                    ch.pixSize = size
                    ch.numDet  = origDetNum*(origSize/size)**2
                    ch.genOptics()
                    msArr.append(self.__clc.calcMappingSpeed(ch)[10])
                msArrArr.append(np.array(msArr))
                #plt.plot(pixSizes*self.__mToMm, np.array(msArr)/np.amax(np.array(msArr)), linewidth=self.__lw, label='%.1f GHz' % (ch.bandCenter*self.__GHz))
                plt.plot(pixSizes*self.__mToMm, np.array(msArr)*self.__uK2, linewidth=self.__lw, label='%.1f GHz' % (ch.bandCenter*self.__GHz))
            yArr = np.sum(msArrArr,axis=0)
            plt.plot(pixSizes*self.__mToMm, yArr*self.__uK2, linewidth=self.__lw, label='Combined')
            plt.title('%s, Pixel %s, F/# = %.2f' % (self.__exp.name, pix, chans[0].Fnumber))
            plt.xlabel('Pixel Size [mm]')
            #plt.ylabel('Normalized Mapping Speed')
            plt.ylabel('Mapping Speed [(uK^2 s)^-1]')
            plt.legend(loc='best', fontsize=24)
            plt.savefig('%s/Pixel_%s_optimize.jpg' % (self.__exp.dir, pix))
            figNum += 1
