#!/usr/local/bin/python

import experiment as exp
import calculation as clc
import noise as nse

#Instantiate classes
sov1  = exp.SOV1()
calc  = clc.Calculation()

#Calculate sensitivity table for SO V1 designs
for so in sov1:
    calc.makeSensTable(so)
