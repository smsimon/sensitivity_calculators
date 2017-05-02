#!/usr/local/bin/python

import pickle as pkl
import matplotlib.pyplot as plt

detPitch, corrFact = pkl.load(open('./PKL/SkyCorrelation_FocalPlanePicture.pkl', 'rb'))

plt.plot(detPitch, corrFact)
plt.show()
