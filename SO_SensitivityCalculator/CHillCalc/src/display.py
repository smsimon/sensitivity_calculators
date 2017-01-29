#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import physics as ph
import calculate as clc

#Class for outputting calculations to tables and plots
class Display:
    def __init__(self, exp):
        #***** Private variables*****
        self.__ph  = ph.Physics() 
        self.__exp = exp
        self.__clc = clc.Calculate(self.__exp)
        self.__freq   = []
        self.__fbw    = []
        self.__numDet = []
        self.__netArr = []
        self.__sens   = []
        self.__ms     = []
        
        #Unit conversions
        self.__GHz    = 1.e-09
        self.__mm     = 1.e+03
        self.__pct    = 1.e+02
        self.__pW     = 1.e+12
        self.__aWrtHz = 1.e+18
        self.__uK     = 1.e+06
        self.__uK2    = 1.e-12

        
    #***** Public Methods *****
    #Create a sensitivity tables
    def textTables(self):
        #Create sensitivity tables for each telescope within the experiment
        print
        print '----------------------------------------------------------------'
        for telescope in self.__exp.telescopes:
            #Output file
            outFile = telescope.dir+'/sensitivityTable.txt'
            f = open(outFile, "w")
            #Write the column titles
            titleStr = str("%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-15s%-11s\n" 
                           % ("Freq", "FBW", "PixSz", "NumDet", "ApertEff", "EdgeTap", "Popt", "NEPph", "NEPbolo", "NEPread", "NEPdet", "NETdet", "NETarr", "Mapping Speed", "Map Depth"))
            unitStr  = str("%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-15s%-11s\n"
                           % ("[GHz]", "", "[mm]", "", "[%]", "[dB]", "[pW]", "[aW/rtHz]", "[aW/rtHz]", "[aW/rtHz]", "[aW/rtHz]", "[uK-rtSec]", "[uK-rtSec]", "[(uK^2 s)^-1]", "[uK-arcmin]"))
            print "***** %s *****" % (telescope.name)
            print titleStr,
            print unitStr,
            f.write(titleStr)
            f.write(unitStr)

            #Calculate loading, optical NEP, bolo NEP, readout NEP,
            #detector NEP, detector NET, and NET array for each channel
            for i in range(telescope.numChans):
                #Load channel
                ch = telescope.chanArr[i]

                #Calculate sensitivity
                cumPower, NEPphoton, NEPbolo, NEPread, NEPTotal, NETphoton, NETbolo, NETread, NET, NETArray, MS, Sens = self.__clc.calcMappingSpeed(ch)
            
                #Isolate aperture efficiency
                ApertEff = ch.effArr[ch.elemArr.index('Aperture')]
                EdgeTaper = 10.*np.log10(1. - ApertEff)
            
                #Write the values to the table
                printStr = str("%-11.1f%-11.2f%-11.1f%-11.0f%-11.2f%-11.2f%-11.2f%-11.2f%-11.2f%-11.2f%-11.2f%-11.2f%-11.2f%-15.4f%-11.2f\n" 
                        % (ch.bandCenter*self.__GHz, ch.fbw, ch.pixSize*self.__mm, ch.numDet, ApertEff*self.__pct, EdgeTaper, cumPower*self.__pW, 
                           NEPphoton*self.__aWrtHz, NEPbolo*self.__aWrtHz, NEPread*self.__aWrtHz, NEPTotal*self.__aWrtHz, NET*self.__uK, 
                           NETArray*self.__uK,  MS*self.__uK2, Sens*self.__uK))
                print printStr,
                f.write(printStr)
                #Store parameters
                self.__freq.append(ch.bandCenter)
                self.__fbw.append(ch.fbw)
                self.__numDet.append(ch.numDet)
                self.__netArr.append(NETArray)
                self.__sens.append(Sens)
                self.__ms.append(MS)
            #Write the total sensitivity
            printStr = str("%-11s%-22s%-11.0f%-88s%-11.2f%-15.4f%-11.2f\n" 
                           % ('Total', '', sum(self.__numDet), '', self.__ph.invVar(self.__netArr)*self.__uK,
                              sum(self.__ms)*self.__uK2, self.__ph.invVar(self.__sens)*self.__uK))
            print printStr
            f.write(printStr)
            f.close()
            
        #Combine all telescopes
        print "***** %s *****" % (self.__exp.name)
        outputFile = self.__exp.dir+'/sensitivityTable.txt'
        f = open(outputFile, 'w')
        #Write the column titles
        titleStr = str("%-11s%-11s%-11s%-11s%-15s%-11s\n"
                % ("Freq", "FBW", "NumDet", "NETarr", "Mapping Speed", "Map Depth"))
        unitStr  = str("%-11s%-11s%-11s%-11s%-15s%-11s\n"
                % ("[GHz]", "", "", "[uK-rtSec]", "[(uK^2 s)^-1]", "[uK-arcmin]"))
        print titleStr,
        print unitStr,
        f.write(titleStr)
        f.write(unitStr)
        #Sort by frequency
        inds = np.argsort(np.array(self.__freq))
        self.__freq   = np.array(self.__freq)[inds]
        self.__fbw    = np.array(self.__fbw)[inds]
        self.__numDet = np.array(self.__numDet)[inds]
        self.__netArr = np.array(self.__netArr)[inds]
        self.__sens   = np.array(self.__sens)[inds]
        self.__ms     = np.array(self.__ms)[inds]
        #Write the values, combining repeat channels
        for i in range(len(self.__freq)):
            if i >= len(self.__freq):
                continue
            #Check for repeat frequencies
            for j in range(i, len(self.__freq)):
                if i == j or j >= len(self.__freq):
                    continue
                if self.__freq[i] == self.__freq[j]:
                    self.__numDet[i] += self.__numDet[j]
                    self.__netArr[i]  = self.__ph.invVar([self.__netArr[i], self.__netArr[j]])
                    self.__sens[i]    = self.__ph.invVar([self.__sens[i], self.__sens[j]])
                    self.__ms[i]      = 1/np.power(self.__netArr[i], 2.)
                    self.__freq   = np.delete(self.__freq, j)
                    self.__fbw    = np.delete(self.__fbw, j)
                    self.__numDet = np.delete(self.__numDet, j)
                    self.__netArr = np.delete(self.__netArr, j)
                    self.__sens   = np.delete(self.__sens, j)
                    self.__ms     = np.delete(self.__ms, j)
            printStr = ("%-11.1f%-11.2f%-11.0f%-11.2f%-15.4f%-11.2f\n" 
                        % (self.__freq[i]*self.__GHz, self.__fbw[i], self.__numDet[i], self.__netArr[i]*self.__uK, self.__ms[i]*self.__uK2,  self.__sens[i]*self.__uK))
            print printStr,
            f.write(printStr)
        
        #Print the totals
        printStr = ("%-11s%-11s%-11.0f%-11.2f%-15.4f%-11.2f\n" 
                    % ('Total', '', sum(self.__numDet), self.__ph.invVar(self.__netArr)*self.__uK, sum(self.__ms)*self.__uK2, self.__ph.invVar(self.__sens)*self.__uK))
        print printStr
        print '----------------------------------------------------------------'
        f.write(printStr)
        f.close()
        
