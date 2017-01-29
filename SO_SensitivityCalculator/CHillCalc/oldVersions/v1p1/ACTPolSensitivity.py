#!/usr/local/bin/python

import experiment as exp
import calculation as clc
import noise as nse

#Instantiate classes
act  = exp.ACTPol()
calc = clc.Calculation()

#Calculate sensitivity table for PB2
calc.makeSensTable(act)
