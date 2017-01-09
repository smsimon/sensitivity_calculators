import numpy as np
class BPStruct:
    def __init__(self, nu, filt, dnu, n):
        self.nu = nu
        self.filt = filt
        self.dnu = dnu
        self.n = n


def bp(nu, deltanu, sigma = 1.0, threshold = 0.001):
    """
    ;  returns a CLASS with bp.nu = vector of freqs in GHz, 
    ;  bp.dnu = stepsize, bp.n = # values of freqs and
    ; bp.filter = a tophat filter convolved with a gaussian of width signma
    ;  -- from looking at cmb5 plots, looks like 1
    ; GHz is a reasonable width
    ;  determines how big a range of nu to return based on the threshold
    ;  value -- nominally set to 0.001"""
    xmax = 5.0 * deltanu + nu
    xmin = nu - 5.0 * deltanu
    nx = xmax - xmin + 1
    if xmin < 0: xmin = 0
    x = np.arange(100*nx)/100. + xmin
#    tophat = x*0
    #set tophat to 1 where x is close to nu, 0 otherwise
    tophat = np.where((x >= nu-deltanu/2.0) * (x <= nu+deltanu/2.0), 
                      np.ones(len(x)), np.zeros(len(x)))
    xg = x - (xmax - xmin)/2.0
    kernel = np.exp(-xg**2/2./sigma**2)
    smallkernel = [] #get rid of small values in kernel that won't matter
    for i in range(len(kernel)):
        if kernel[i] > threshold: smallkernel.append(kernel[i])
    #WARNING: correlate NOT functionally identical to convol in IDL
    #convol pads zeros at edges, whereas correlate does not
    #as far as I know, no other differences exist
    result = np.correlate(tophat, smallkernel, mode = 'same')
    useband = []
    for i in range(len(result)):
        if result[i] > threshold: useband.append(i)
    result = result[useband] #gets rid of values too small to matter
    nuvec = x[useband]
    result = result/np.max(result)
    dnu = nuvec[1] - nuvec[0]
    n = len(nuvec)
    return BPStruct(nu = nuvec, filt = result, dnu = dnu, n = n)
    
