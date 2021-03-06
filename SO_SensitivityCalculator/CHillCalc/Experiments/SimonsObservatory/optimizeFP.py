#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import experiment as exp
import optimize as opt
import glob as gb

#Define which design to calculate
designDir = './Designs/V2_dichroic/'
plotInMM = True

#Define the atmosphere
atmFile = './Atacama_1000um_60deg.txt'

#Gather experiments
#designDirs  = sorted(gb.glob(designDir+'/*/'))
designDirs  = sorted(gb.glob(designDir+'/MF_45cm_7waf_silicon/'))
experiments = [exp.Experiment(dir, atmFile) for dir in designDirs]

#Optimize pixel sizes
optimizes   = [opt.Optimize(experiment) for experiment in experiments]
for optimize in optimizes: optimize.optimizeFP(plotInMM)
