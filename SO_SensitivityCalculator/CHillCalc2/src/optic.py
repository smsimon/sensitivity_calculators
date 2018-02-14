#python Version 2.7.2
import numpy     as np
import parameter as pr
import physics   as ph
import units     as un
import band      as bd

class Optic:
    def __init__(self, log, dict, nrealize=1, bandFile=None):
        self.__ph = ph.Physics()
        self.log      = log
        self.bandFile = bandFile
        self.nrealize = nrealize

        #Store optic parameters
        self.element      =              dict['Element']
        self.temper       = pr.Parameter(dict['Temperature'])
        self.absorb       = pr.Parameter(dict['Absorption'])
        self.refl         = pr.Parameter(dict['Reflection'])
        self.thick        = pr.Parameter(dict['Thickness'],     un.mmToM)
        self.index        = pr.Parameter(dict['Index'])
        self.lossTan      = pr.Parameter(dict['Loss Tangent'],  1.e-04)
        self.conductivity = pr.Parameter(dict['Conductivity'],  1.e+06)
        self.surfaceRough = pr.Parameter(dict['Surface Rough'], un.umToM)
        self.spill        = pr.Parameter(dict['Spillover'])
        self.spillTemp    = pr.Parameter(dict['Spillover Temp'])
        self.scattFrac    = pr.Parameter(dict['Scatter Frac'])
        self.scattTemp    = pr.Parameter(dict['Scatter Temp'])    

    #***** Private Functions *****
    #Ratio of blackbody power between two temperatures
    def __powFrac(self, T1, T2, freqs):
        return np.trapz(self.__ph.bbPowSpec(freqs, T1), freqs)/np.trapz(self.__ph.bbPowSpec(freqs, T2), freqs)

    #Power spilled over the primrary mirror
    def __primarySpill(self, ch):
        et = -self.__ph.edgeTaper(self.__ph.spillEff(ch.bandCenter.getAvg(), ch.pixSize, ch.Fnumber, ch.wf))
        freq = ch.bandCenter*un.HzToGHz
        #Primary spillover values for the SO 45 cm LATR
        params = np.array([[  8.99403547e-10,  -5.94688018e-07,   1.89966392e-04],
                           [ -4.43582650e-08,   2.72620964e-05,  -7.15209427e-03],
                           [  6.03942212e-07,  -3.45691036e-04,   7.81613979e-02]])
        pams = []
        for i in range(len(params)):
            p = np.poly1d(params[i])
            pams.append(p(freq))
        p = np.poly1d(pams)
        y = p(et)
        if y < 0.: y = 0.
        return y

    #***** Public Functions *****
    #Generate element, temperature, emissivity, and efficiency
    def generate(self, ch):
        def samp(param, bandID=ch.bandID, pos=True, norm=False): 
            if self.nrealize == 1: return param.getAvg(bandID)
            else:                  return param.sample(bandID=bandID, nsample=1, pos=pos, norm=norm)

        #Temperature
        temp = samp(self.temper); temp  = [temp for f in ch.freqs]

        #Efficiency from a band file?
        if self.bandFile is not None:
            band = bd.Band(self.log, self.bandFile, ch.freqs)
            eff  = band.sample()[0]
            if eff is not None:
                eff = np.array([e if e > 0 else 0. for e in eff])
                eff = np.array([e if e < 1 else 1. for e in eff])
                #for e in eff:
                #    if e > 1: e = 1.
                #    if e < 0: e = 0.
        else: 
            eff = None

        #Reflection
        if eff is None:
            if not self.refl.isEmpty():                                 refl = samp(self.refl, norm=True); refl = np.array([refl for f in ch.freqs])
            elif 'Mirror' in self.element or 'Primary' in self.element: refl = 1. - self.__ph.ruzeEff(ch.freqs, samp(self.surfaceRough))
            else:                                                       refl = 0.; refl = np.array([refl for f in ch.freqs])

        #Spillover
        if not self.spill.isEmpty():     spill     = samp(self.spill, norm=True);
        elif 'Primary' in self.element:  spill     = self.__primarySpill(ch)
        else:                            spill     = 0.
        spill = np.array([spill for f in ch.freqs])
        if not self.spillTemp.isEmpty(): spillTemp = samp(self.spillTemp); spillTemp = np.array([spillTemp for f in ch.freqs])
        else:                            spillTemp = np.array([temp for f in ch.freqs])

        #Scattering
        if not self.scattFrac.isEmpty(): scatt     = samp(self.scattFrac, norm=True)
        else:                            scatt     = 0.
        scatt = np.array([scatt for f in ch.freqs])
        if not self.scattTemp.isEmpty(): scattTemp = samp(self.scattTemp); scattTemp = np.array([scattTemp for f in ch.freqs])
        else:                            scattTemp = np.array([temp for f in ch.freqs])

        #Absorption
        if 'Aperture' in self.element:
            if not eff: 
                if not self.absorb.isEmpty(): abso = samp(self.absorb, norm=True); abso = np.array([abso for f in ch.freqs])
                else:                         abso = 1. - self.__ph.spillEff(ch.freqs, ch.pixSize, ch.Fnumber, ch.wf)
            else:       
                abso = 1. - eff
        else:
            if not self.absorb.isEmpty():                               abso = samp(self.absorb, norm=True); abso = np.array([abso for f in ch.freqs])
            elif 'Mirror' in self.element or 'Primary' in self.element: abso = 1. - self.__ph.ohmicEff(ch.freqs, samp(self.conductivity))
            else:                                                       abso = self.__ph.dielectricLoss(ch.freqs, samp(self.thick), samp(self.index), samp(self.lossTan))
        
        #Reflection from band file?
        if eff is not None: 
            refl = 1. - eff - abso
            for r in refl:
                if r > 1: r = 1.
                if r < 0: r = 0.
        
        #Element, absorption, efficiency, and temperature
        elem  = self.element
        if not scatt is None and not spill is None: emiss = abso + scatt*refl*self.__powFrac(scattTemp, temp, ch.freqs) + spill*self.__powFrac(spillTemp, temp, ch.freqs)
        elif not spill is None:                     emiss = abso + spill*self.__powFrac(     spillTemp, temp, ch.freqs) 
        elif not scatt is None:                     emiss = abso + scatt*refl*self.__powFrac(scattTemp, temp, ch.freqs)
        else:                                       emiss = abso
        if not eff is None: effic = eff - spill
        else:               effic = 1. - refl - abso - spill

        #Store channel pixel parameters
        if elem == 'Aperture':
            ch.apEff     = np.trapz(effic, ch.freqs)/(ch.freqs[-1] - ch.freqs[0])
            ch.edgeTaper = self.__ph.edgeTaper(ch.apEff)

        return [elem, emiss, effic, temp]

