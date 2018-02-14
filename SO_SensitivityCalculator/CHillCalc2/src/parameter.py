#python Version 2.7.2
import numpy as np

class Parameter:
    def __init__(self, input, unit=1.0):
        self.__spreadDelim = '+/-'
        
        self.inst = input
        self.unit = unit

        if self.__spreadDelim in input:
            vals     = input.split(self.__spreadDelim)
            self.avg = self.__float(vals[0], self.unit)
            self.std = self.__float(vals[1], self.unit)
        else:
            self.avg = self.__float(input,   self.unit)
            self.std = self.__zero(self.avg)

    #***** Public Methods *****
    def isEmpty(self):
        if 'NA' in str(self.avg): return True
        else:                     return False

    def convolve(self, param):
        if not self.isEmpty() and not param.isEmpty():
            self.avg = self.avg*param.avg
            self.std = np.sqrt(self.std**2 + param.std**2)

    def multiply(self, factor):
        if not self.isEmpty():
            self.avg = self.avg*factor
            self.std = self.std*factor
    
    def fetch(self, bandID=1):
        if self.isEmpty():
            return ('NA', 'NA')
        else:
            if 'array' in str(type(self.avg)): return (self.avg[bandID-1], self.std[bandID-1])
            else:                              return (self.avg,           self.std          )

    def getAvg(self, bandID=1):
        return self.fetch(bandID)[0]
    
    def getStd(self, bandID=1):
        return self.fetch(bandID)[1]

    def sample(self, bandID=1, nsample=1, pos=False, norm=False, min=None, max=None):
        if self.isEmpty(): 
            return 'NA'
        else:
            avg, std = self.fetch(bandID)
            if std <= 0.: return avg
            else:         
                if nsample == 1: samp = np.random.normal(avg, std, nsample)[0]
                else:            samp = np.random.normal(avg, std, nsample)
                
            if min is not None: 
                if samp < min: return min
            if max is not None:
                if samp > max: return max

            if   pos and norm:
                if   samp < 0: return 0.
                elif samp > 1: return 1.
                else:          return samp
            elif pos:
                if samp < 0:   return 0.
                else:          return samp
            elif norm:
                if samp > 1:   return 1.
                else:          return samp
            else:
                return samp

    #***** Private Methods *****
    def __float(self, val, unit=1.0):
        try:
            return unit*float(val)
        except:
            try:
                return unit*np.array(eval(val)).astype(np.float)
            except:
                return str(val)

    def __zero(self, val):
        try:
            return np.zeros(len(val))
        except:
            return 0.
