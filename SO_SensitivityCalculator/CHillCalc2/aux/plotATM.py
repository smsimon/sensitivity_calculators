#Using python 2.7.2
import matplotlib.pyplot as plt
import numpy as np
import sys

#ATM file passed at the command line
try:
    atmFile = sys.argv[1]
except:
    print 'Usage: python plotATM.py [atm text file]'
    print 'ATM files should have tab-separated columns: Freq [GHz]   RJ Temp [K]   Optical Depth   Transmission'
    print
    sys.exit(1)

#Read in ATM data
freqArr, transArr = np.loadtxt(atmFile, usecols=[0,3], unpack=True)

#Frequency bands to overplot
freqs = np.array([27.,   39.,   93.,   145.,  225.,  278.])
bws   = np.array([0.222, 0.462, 0.376, 0.276, 0.267, 0.162])

freqLo = freqs*(1 - 0.5*bws)
freqHi = freqs*(1 + 0.5*bws)

plt.rc('font', family='serif')
plt.rc('font', size=32)
lw=4

plt.figure(0, figsize=(15,10))
plt.plot(freqArr, transArr,  'k-', linewidth=lw)
for i in range(len(freqs)):
    plt.axvspan(freqLo[i], freqHi[i], linewidth=0, color='r', alpha=0.5)
plt.title('Atmosphere')
plt.xlim([freqLo[0]-5, freqHi[-1]+5])
plt.ylabel('Transmssion')
plt.xlabel('Frequency [GHz]')
plt.savefig('ATMTransmission.jpg')
