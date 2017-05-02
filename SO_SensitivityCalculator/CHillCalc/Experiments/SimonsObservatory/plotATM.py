#!/usr/local/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Read in ATM data
freqArr, transArr = np.loadtxt('Atacama_1000um_60deg.txt', usecols=[0,3], unpack=True)

#Frequency bands to overplot
freqs = np.array([27.,   39.,   93.,   145.,  233.,  225.,  278.])
bws   = np.array([0.222, 0.462, 0.376, 0.276, 0.322, 0.267, 0.162])

freqLo = freqs*(1 - 0.5*bws)
freqHi = freqs*(1 + 0.5*bws)

plt.rc('font', family='serif')
plt.rc('font', size=32)
lw=4

plt.figure(0, figsize=(15,10))
plt.plot(freqArr, transArr,  'k-', linewidth=lw)
for i in range(len(freqs)):
    plt.axvspan(freqLo[i], freqHi[i], linewidth=0, color='r', alpha=0.5)
plt.title('Atmosphere Assumption')
plt.xlim([freqLo[0]-5, freqHi[-1]+5])
plt.ylabel('Transmssion')
plt.xlabel('Frequency [GHz]')
plt.savefig('ATMTransmission.jpg')
