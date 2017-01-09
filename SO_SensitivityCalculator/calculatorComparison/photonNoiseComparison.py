#!/usr/local/bin/python

import numpy as np
import scipy.constants as sp
import scipy.integrate as itg
import matplotlib.pyplot as plt

#Photon power spectrum on a diffraction-limited detector
def popt(freq, temp):
    return 0.5*((sp.c/freq)**2)*(2*sp.h*(freq**3)/float(sp.c**2))*(1./(np.exp((sp.h*freq)/float(sp.k*temp)) - 1.))

#Charlie's photon noise
def cah(f1, f2, T):
    NEPph = np.sqrt(itg.quad(lambda x: 2*sp.h*x*popt(x, T) + 2*popt(x, T)**2, f1, f2)[0])
    return NEPph

#Sarah Marie's photon noise
def smb(f1, f2, T):
    f0 = (f1 + f2)/2.
    df = (f2 - f1)
    pow = itg.quad(lambda x: popt(x, T), f1, f2)[0]
    print pow
    NEPshot  = np.sqrt(2.*sp.h*f0*pow)
    NEPdicke = np.sqrt(2.*(pow**2)/df)
    NEPph = np.sqrt(NEPshot**2 + NEPdicke**2)
    return NEPph

#Compare the two
TArr  = np.array([4., 10., 50.])
lsArr = ['-', '--', ':']
fCent = np.linspace(90., 350., 10)*1.e9
fbw   = 0.3
f1Arr = fCent*(1. - 0.5*fbw)
f2Arr = fCent*(1. + 0.5*fbw)

#Overplot the two
plt.figure(0, figsize=(15, 12))
plt.rc('font', size=32)
plt.rc('font', family='serif')
lw = 3

for i in range(len(TArr)):
    cahArr = np.array([cah(f1Arr[j], f2Arr[j], TArr[i]) for j in range(len(fCent))])
    smbArr = np.array([smb(f1Arr[j], f2Arr[j], TArr[i]) for j in range(len(fCent))])
    plt.plot(fCent*1.e-9, (cahArr/np.amax(cahArr)), linewidth=lw, color='b', linestyle=lsArr[i])
    plt.plot(fCent*1.e-9, (smbArr/np.amax(smbArr)), linewidth=lw, color='r', linestyle=lsArr[i])

plt.title("All FBW = 0.3")
plt.ylabel("Photon NEP [aW/rtHz]")
plt.xlabel("Frequency [GHz]")
#plt.legend(loc='best', fontsize=24)
plt.savefig("photonNoiseComparison.jpg")
