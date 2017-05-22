#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import experiment as exp
import optimize as opt
import glob as gb

#Define which design to calculate
designDir = './Designs/V2_TokiS4Bands/'

#Define the atmosphere
atmFile = './Atacama_1000um_60deg.txt'

#Gather experiments
designDirs  = sorted(gb.glob(designDir+'/*/'))
print designDirs
experiments = [exp.Experiment(dir) for dir in designDirs]

#Optimize pixel sizes
optimizes   = [opt.Optimize(experiment) for experiment in experiments]
for optimize in optimizes: optimize.optimizeFP()
