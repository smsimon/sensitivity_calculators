#!/usr/local/bin/python

import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt

#Charlie's bolometer noise
def cah(psat, n, Tb, Tc):
    return np.sqrt(4*sp.k*psat*Tb*(((np.power((n+1),2.)/((2*n)+3))*((np.power((Tc/Tb),((2*n)+3)) - 1)/np.power((np.power((Tc/Tb),(n+1)) - 1),2.)))))

#Sarah Marie's boloemter noise
def smb(psat, n, Tb, Tc, flink=1.):
    return np.sqrt(4.*sp.k*flink*(Tc**2)*(n*(Tc**(n-1.))*psat)/((Tc**n) - (Tb**n)))

#Compare the two
n = 2.7
Tb = 0.100
psat = 8.e-12
TcArr = np.linspace(0.110, 0.300, 100)
cahArr = np.array([cah(psat, n, Tb, Tc) for Tc in TcArr])
smbArr = np.array([smb(psat, n, Tb, Tc) for Tc in TcArr])

#Overplot the two
plt.figure(0, figsize=(15, 12))
plt.rc('font', size=32)
plt.rc('font', family='serif')
lw = 3

plt.plot(TcArr*1.e3, cahArr*1.e18, linewidth=lw, label="CHillCalc", color='b', linestyle='-')
plt.plot(TcArr*1.e3, smbArr*1.e18, linewidth=lw, label="NETBook",   color='r', linestyle='-')
plt.title("n = 2.7, Tb = 100 mK, psat = 8 pW")
plt.ylabel("Bolo NEP [aW/rtHz]")
plt.xlabel("Tc [mK]")
plt.legend(loc='best', fontsize=24)
plt.savefig("boloNoiseComparison.jpg")
