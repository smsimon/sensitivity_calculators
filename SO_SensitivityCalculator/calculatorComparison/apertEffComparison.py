
import numpy as np

#SO V1 designs
names = np.array(['V1La', 'V1La_2', 'V1Lb', 'V1Ld', 'V1Ld_2', 'V1p1', 'V1p2'])

#Pixel size, in F-lambda, for each design
diam = np.array([1.77, 1.77, 1.61, 1.46, 1.70, 1.37, 1.47])

#Waist ratios to consider
wfArr = np.array([2.6, 3.2])

#Equation to calculate apert eff
def eff(wf, d):
    return 1 - np.exp(-((np.pi**2)/2.)*((d/wf)**2))

#Mike's efficiencies
mike = np.array([0.74, 0.74, 0.68, 0.65, 0.71, 0.60, 0.65])

#Calculate for various waist parameters
#wf = 2.6
eff_1 = np.array([float('%.2f' % eff(2.6, d)) for d in diam])
#wf = 3.2
eff_2 = np.array([float('%.2f' % eff(3.2, d)) for d in diam])

#Print the values
print 'Design:  ', names
print 'Mike:    ', mike
print 'wf = 2.6:', eff_1
print 'wf = 3.2:', eff_2

