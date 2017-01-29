#!/usr/local/bin/python

import experiment as exp
import calculation as clc
import noise as nse

#Instantiate classes
pb2  = exp.PB2()
calc = clc.Calculation()

#Calculate sensitivity table for PB2
calc.makeSensTable(pb2)
