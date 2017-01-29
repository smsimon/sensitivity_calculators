#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import experiment as exp
import display as dsp
import optimize as opt
import glob as gb

#Assumed directory structure
# -- 'Designs'
#   -- V1 Pixel size protocols
#      -- V1 designs

#Define the atmosphere
atmFile = './Atacama_1000um_60deg.txt'

#Gather experiments
designDirs = [sorted(gb.glob(x+'/*')) for x in sorted(gb.glob('./Designs/*/'))]
experiments = [[exp.Experiment(dir) for dir in dirs] for dirs in designDirs]
displays    = [[dsp.Display(experiment) for experiment in exps] for exps in experiments] 
for i in range(len(designDirs)):
    for j in range(len(designDirs[i])): 
        dsp = displays[i][j]
        dsp.textTables()
    print
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print
