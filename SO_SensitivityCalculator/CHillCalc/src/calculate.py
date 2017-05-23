#!/usr/local/bin/python

#Class for claculating sensitivity

#python Version 2.7.2
import numpy as np
import physics as phy
import noise as nse

class Calculate:
    def __init__(self, exp, corr=False):
        #***** Private variables *****
        self.__ph  = phy.Physics()
        self.__nse = nse.Noise()
        self.__exp = exp
        self.__corr = corr

        #Unit conversions
        self.__GHz    = 1.e-09
        self.__mm     = 1.e+03
        self.__pct    = 1.e+02
        self.__pW     = 1.e+12
        self.__aWrtHz = 1.e+18
        self.__uK     = 1.e+06
        self.__uK2    = 1.e-12

        #Directory for writing result tables
        self.__dir = self.__exp.dir+'/TXT/'

    #***** Public methods *****
    #Calculate total in-band optical power for a given channel [W]
    def calcPopt(self, ch):
        #Need an extra efficiency for the calculation
        effArr = np.insert(ch.effArr, len(ch.effArr), 1.0)

        #Photon powers
        cumPower = 0 #Total power
        skyPower = 0 #Power from the sky
        rvrPower = 0 #Power from the receiver
        hwpPower = 0 #Power from the HWP
        
        #Efficiencies
        totEff = 0 #End-to-end efficiency
        rvrEff = 0 #Receiver efficiency
        hwpEff = 0 #Efficiency of everything detector-side of the HWP
        
        #Run the calculation
        for j in range(len(ch.elemArr)):
            #Element
            elem = str(ch.elemArr[j])
            #Element emissivity
            elemEmm = float(ch.emissArr[j])
            #Element temperature
            elemTemp = float(ch.tempArr[j])
            #Efficiency of everything detector-side of the element
            cumEff = reduce(lambda x, y: float(x)*float(y), effArr[j+1:])
            if j == 0:
                totEff = cumEff
            if j == 1:
                rvrEff = cumEff
            if 'HWP' in elem:
                hwpEff = cumEff
            #Add power seen at detector from that element
            pow = self.__ph.bbPower(elemEmm*cumEff, ch.bandCenter, ch.fbw, elemTemp, ch.nModes)
            cumPower += pow
            if j < 2:
                skyPower += pow
            else:
                rvrPower += pow
            if 'HWP' in elem:
                hwpPower = pow

        return cumPower, skyPower, rvrPower, hwpPower, totEff, rvrEff, hwpEff

    #Calculate Psat/Popt
    def calcETF(self, ch):
        if ch.psat != 'NA':
            return ch.psatFact
        else:
            cumPower = self.calcPopt(ch)[0]
            return ch.psat/cumPower

    #Calculate photon NEP
    def calcPhotonNEP(self, ch):
        #Need an extra efficiency for the calculation
        effArr = np.insert(ch.effArr, len(ch.effArr), 1.0)

        #Calculate cumulative photon power
        powerFrom    = [] #Power from this element onto the detector
        powerTo      = [] #Power on this element from sky-side elements
        cumPowerIntegrands = []
        cumPower = 0

        #Store the power from each element
        powers     = []
        effSkySide = []
        effDetSide = []
        for j in range(len(ch.elemArr)):
            #Element emissivity
            elemEmm = float(ch.emissArr[j])
            #Element temperature
            elemTemp = float(ch.tempArr[j])
            #Detector-side efficiency
            cumEffDet = reduce(lambda x, y: float(x)*float(y), effArr[j+1:])
            effDetSide.append(cumEffDet)
            #Sky-side efficiencies
            cumEffSky = [reduce(lambda x, y: float(x)*float(y), effArr[i+1:j-1]) if i+1 < j-1 else 1. for i in range(j-1)] + [0.]
            #if j > 1:    cumEffSky = [reduce(lambda x, y: float(x)*float(y), effArr[i:j]) if i < j-1 else 1. for i in range(j)] + [0.]
            #elif j == 1: cumEffSky = [1.] + [0.]
            #else:        cumEffSky = []   + [0.]
            effSkySide.append(cumEffSky)
            #Add power emitted from this element
            pow = self.__ph.bbPower(elemEmm, ch.bandCenter, ch.fbw, elemTemp, ch.nModes)
            powers.append(pow)
            
        #Store other stuff
        for j in range(len(ch.elemArr)):
            #Element emissivity
            elemEmm = float(ch.emissArr[j])
            #Element temperature
            elemTemp = float(ch.tempArr[j])
            #Efficiency of everything detector-side of the element
            #cumEff = reduce(lambda x, y: float(x)*float(y), effArr[j+1:])
            #Add power seen at detector from that element
            #pow = self.__ph.bbPower(elemEmm*cumEff, ch.bandCenter, ch.fbw, elemTemp, ch.nModes)
            powOut = powers[j]*effDetSide[j]
            powerTo.append(powOut)
            cumPower += powOut
            powIn = sum([powers[k]*effSkySide[j][k] for k in range(j-1)])
            powerFrom.append(powIn)
            #Add cumulative power integrand to array for each element
            cumPowerIntegrands.append(lambda f, elemEmm=elemEmm, cumEff=effDetSide[j], elemTemp=elemTemp, nModes=ch.nModes: self.__ph.bbPowSpec(elemEmm*cumEff, f, elemTemp, ch.nModes))

        #Photon NEP
        NEP_ph, NEP_pharr = self.__nse.photonNEP(cumPowerIntegrands, ch.bandCenter, ch.fbw)
        
        #Return optical power and photon noise
        return powerFrom, powerTo, cumPower, NEP_ph, NEP_pharr

    #Calculate mapping speed [(K^2-sec)^-1]
    def calcMappingSpeed(self, ch, corr=None):
        if not corr:
            corr = self.__corr
        #Need an extra efficiency for the calculation
        effArr = np.insert(ch.effArr, len(ch.effArr), 1.0)
        #Efficiency of full optical path
        skyEff = reduce(lambda x, y: float(x)*float(y), effArr) 

        #Photon noise and optical power
        if corr:
            powIn, powOut, cumPower = self.calcPhotonNEP(ch)[:3]
            cumPowerIntegrands = []
            for j in range(len(ch.elemArr)):
                elemEmm = float(ch.emissArr[j])
                cumEff = float(np.prod(effArr[j+1:]))
                elemTemp = float(ch.tempArr[j])
                cumPowerIntegrands.append(lambda f, elemEmm=elemEmm, cumEff=cumEff, elemTemp=elemTemp, nModes=ch.nModes: self.__ph.bbPowSpec(elemEmm*cumEff, f, elemTemp))
            NEP_ph, NEP_pharr           = self.__nse.photonNEP(cumPowerIntegrands, ch.bandCenter, ch.fbw, ch.elemArr, ch.numDet, (ch.pixSize/(ch.Fnumber*self.__ph.lamb(ch.bandCenter))))
        else:
            powIn, powOut, cumPower, NEP_ph, NEP_pharr = self.calcPhotonNEP(ch)            
        NET_ph = self.__nse.NETfromNEP(NEP_ph, ch.bandCenter, ch.fbw, skyEff)
        #Bolometer noise
        if ch.psat == 'NA':
            NEP_bolo = self.__nse.bolometerNEP(ch.psatFact*cumPower, ch.n, ch.Tc, ch.Tb)
        else:
            NEP_bolo = self.__nse.bolometerNEP(ch.psat, ch.n, ch.Tc, ch.Tb)
        NET_bolo = self.__nse.NETfromNEP(NEP_bolo, ch.bandCenter, ch.fbw, skyEff)
        #Readout noise
        if ch.nei == 'NA':
            NEP_rd = np.sqrt(0.21)*np.sqrt(NEP_ph**2 + NEP_bolo**2)
        else:
            if ch.psat == 'NA':
                NEP_rd = self.__nse.readoutNEP((ch.psatFact - 1.0)*cumPower, ch.boloR, ch.nei)
            else:
                NEP_rd = self.__nse.readoutNEP(ch.psat, boloR, nei)
        NET_rd = self.__nse.NETfromNEP(NEP_rd, ch.bandCenter, ch.fbw, skyEff)
        #Total noise
        NEP     = np.sqrt(NEP_ph**2    + NEP_bolo**2 + NEP_rd**2)
        NEP_arr = np.sqrt(NEP_pharr**2 + NEP_bolo**2 + NEP_rd**2)
        NET     = self.__nse.NETfromNEP(NEP,     ch.bandCenter, ch.fbw, skyEff)*self.__exp.netMgn
        NET_arr = self.__nse.NETfromNEP(NEP_arr, ch.bandCenter, ch.fbw, skyEff)*self.__exp.netMgn
        #NET array
        NETarr = self.__nse.NETarr(NET_arr, ch.numDet, ch.detYield)
        #Sensitivity
        Sens = self.__nse.sensitivity(NETarr, self.__exp.fsky, self.__exp.tobs*self.__exp.obsEff)
        #Mapping speed
        MS = self.__nse.mappingSpeed(NET_arr, ch.numDet, ch.detYield)

        return powIn, powOut, cumPower, NEP_ph, NEP_bolo, NEP_rd, NEP, NET_ph, NET_bolo, NET_rd, NET, NETarr, MS, Sens
