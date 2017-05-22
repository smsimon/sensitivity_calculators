#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import experiment as exp
import display as dsp
import optimize as opt
import glob as gb

#Design directory to calculate
designDir = './Designs/V2_dichroic/'

#Define the atmosphere
atmFile = './Atacama_1000um_60deg.txt'
correlations = False

#Gather experiments
designDirs  = [sorted(gb.glob(x+'/*')) for x in sorted(gb.glob(designDir))]
experiments = [[exp.Experiment(dir, atmFile) for dir in dirs] for dirs in designDirs]
displays    = [[dsp.Display(experiment, correlations) for experiment in exps] for exps in experiments] 
for i in range(len(designDirs)):
    print '%s' % (designDirs[i][0].split('/')[2])
    for j in range(len(designDirs[i])): 
        dsp = displays[i][j]
        dsp.textTables()
    print
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print '**********************************************************************************************************************'
    print
