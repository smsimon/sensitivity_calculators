#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import experiment as exp
import display as dsp
import optimize as opt
import glob as gb

#Define the atmosphere
atmFile = './Atacama_1000um_60deg.txt'

#Gather experiments
designDirs = sorted(gb.glob('./Designs/*/'))
experiments = [exp.Experiment(dir, atmFile) for dir in designDirs]
displays    = [dsp.Display(experiment) for experiment in experiments]
#optimizes   = [opt.Optimize(experiment) for experiment in experiments]
for i in range(len(designDirs)):
    dsp = displays[i]
    dsp.textTables()
    print
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print
