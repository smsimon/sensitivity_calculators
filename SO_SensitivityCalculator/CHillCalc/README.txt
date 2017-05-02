##########################

'CHillCalc' was  written in full by Charles Hill at UC Berkeley
Publish date = 2016-12-07
Latest revision = 3.0
Latest revision date = 2017-05-02

##########################

REVISION HISTORY

* 3.0 on 2017-05-02 -- addition of V2 designs and implementation of white noise correlations
* 2.0 on 2017-01-29 -- significant rewriting and restructuring to handle even more general experimental configurations
* 1.1 on 2017-01-08 -- upgraded to take configuration files for arbitrary experiments. Now, nothing about a CMB instrument is hardcoded - all information is taken from config files
* 1.0 on 2016-12-07 -- a stripped-down version of the sensitivity portion of Charlie's personal sensitivity code, meant only to calculate NET and MS for Simons Observatory

##########################

OVERVIEW

CHillCalc is designed to take input parameters for an experiment and return NET and Mapping Speed for that experiment. It's been primarily used for POLARBEAR-2 and LiteBIRD forecasting, but it can make white-noise estimates for any experiment.

##########################

EXPERIMENT FILE STRUCTURE

Experiments can be found in the './Experiments' directory. The top-down structure for the experiment directory goes as
(1) Experiment (i.e. SimonsArray or SimonsObservatory)
    -- '%s_%d_%d.txt' % (site, um PWV, deg elevation) contains the atmosphere spectrum
    -- 'calc.py' calculates sensitivity for all V2_dichroic optical designs associated with this experiment
       -- To change which sensitivities are calculated (e.g. V1 instead of V2), edit the variable 'designDir' in the 'calc.py' source file
    -- 'optimizeFP.py' calculates the mapping-speed vs pixel size curve for all V2_dichroic optical designs associated with this experiment
       -- To change which sensitivities are calculated (e.g. V1 instead of V2), edit the variable 'designDir' in the 'optimizeFP.py' source file
(2) Experimental Designs (i.e. SO V2_dichroic configurations)
(3) Telescopes (for SO, there is only one telescope as of v3.0 of this code, but we will likely add more soon)
    -- 'experiment.txt' contains parameters that are same for all telescopes (e.g. observation time)
(3) Config files for a telescope
    -- 'camera.txt' contains parameters common to the reimaging optics or the focal plane
    -- 'opticalChain.txt' contains all optics within the telescope and describes their properties
    -- 'channels.txt' contains all frequency channels in the camera and describes their properties

##########################

EXPERIMENT.TXT

-- ObservationTime = number of years the experiment will observe the CMB
-- SkyFraction = the fraction of the sky that the experiment will map
-- ObservationEfficiency = effective observation time is ObservationTime*ObservationEfficiency
-- NETmargin = the NET of any detector channel is the (caculated NET)*NETmargin

##########################

CAMERA.TXT

This file contains parameters that are common to all channels within the camera

-- OpticalCouplingToFP = an overall factor for how well the focal plane couples to the optics (e.g. Strehl)
-- Fnumber = detector F/#
-- BathTemp = base temperature for this telesope's focal plane

##########################

OPTICALCHAIN.TXT

This file contains information about all of the optics within the telescope. In the absence of information, the entry must be 'NA'. 
Note that this file does not contain information about the sky or the detector channels.

If the parameter is given by a single number, the value is the same for all frequency channels. If the parameter is given by a list, then
the value depends on frequency channel. Therefore, the values should then be entered into the list as 

**list index = (band ID - 1) from CHANNELS.TXT**

-- Element = optic name
-- Temp = (average) temperature, used to cacluate emitted power
-- Thick = (average) thickness, used to cacluate absorption
-- Index = (average) index of refraction, used to calculate absorption
-- LossTan = (average) dielectric loss tangent, used to calculate absorption
-- Conduct = metal conductivity, used to calculate absorption in reflectors
-- Absorb = specified absorption. Having an entry here will ignore 'Thick', 'Index', and 'LossTan'
-- SurfaceRough = RMS surface roughness used to caculate surface scattering off reflectors
-- Refl = reflection
-- ScattFrac = the fraction of reflected light 'Refl' that is scattered to somewhere other than back to the focal plane
-- ScattTemp = the temperature of the surface upon which the scattered light lands

##########################

CHANNELS.TXT

This file contains information regarding the frequency channels and their detectors. In the absence of information, the entry must be 'NA'.

-- BandID = band name
-- PixelID = name of pixel this band is on
-- BandCenter = central frequency of the frequency band
-- FBW = band fractional bandwidth (freqHi - freqLo)/BandCenter
-- PixSize = pixel diameter, or equivilantly spacing between pixels on the focal plane
-- NumDet = number of detectors for this frequency channel in this telescope
-- WaistFact = equivalent to 'w_f', which defines the ratio of the pixel diameter 'D' to its gaussian beam waist size 'w_0'
-- DetEff = detector efficiency, including antenna performance, microstrip loss, impedance mismatch at the load resistor, etc.
-- Psat = saturation power
-- PsatFact = If 'Psat' is 'NA', then Psat = PsatFact*Popt (see below)
-- CarrierIndex = thermal carrier index for bolometer thermal conduction
-- TransTemp = Bolometer transition/operation temperature
-- TcFrac = If 'TransTemp' is 'NA', then TransTemp = TcFrac*(Bath Temperature)
-- BunchFactor = a weighting for the Dicke factor in the photon noise term. As of 2017-05-02, this should always be 1.0. (I'll phase this out eventually...)
-- Yield = detector yield for this channel
-- NEI = noise equivalent current for this channel. If 'NA', readout noise contributes only 10% to the total noise (recall that NEP's are added in quadrature)
-- nModes = number of modes read out by a detector on this channel. Can become greater than 1.0 if the pixel is too large. As of 2017-05-02, this should always be 1.0.
-- boloR = bolometer resistance (used to calculate readout noise)

##########################

EXECUTABLES

Within each experiment directory, there are the following executables

-- 'calc.py' gathers directories at the design level (i.e. the folder that contains the 'experiment.txt' config file and the telescope directories), 
   creates 'Experiment' and 'Display' objects, calculates experimental sensitivity, and outputs the sensitivity tables both to the terminal and to files called 'sensitivityTable.txt'

-- 'optimizeFP.py' takes directories at the design level, creates 'Experiment', and 'Optimize' objects, and calculates mapping speed 
   as a function of pixel spacing and writes the result to plots and ASCII files

##########################

SETTING THE ENVIRONMENT

Before running any executables, you must set the environment from the calculator's home directory 'CHillCalc/'

If you are using bash, run the command:
'source env.sh'

and if you are running tcsh:
'source env.csh'

##########################

ALTERING AN EXISTING EXPERIMENT

There are only four files you can edit to adjust the parameters of an existing experiment:
  -- 'experiment.txt'
  -- 'camera.txt'
  -- 'opticalChain.txt'
  -- 'channels.txt'

See above for information about what is in these files

##########################

BUILDING YOUR OWN EXPERIMENT

To build your own experiment or create a new design, you must follow this file structure
  -- Design/
  -- Within the 'Design/' directory...
       -- Your design directories (the names of these design directories are used to name the 'Experiment' objects)
       -- A 'calc.py' executable
  -- Within each of your created design directories...
       -- 'experiment.txt' 
       -- Your telescope directories (the names of these telescope directories are used to name the 'Telescope' objects)
  -- Within each of your telescope directories...
       -- 'camera.txt' 
       -- 'opticalChain.txt'
       -- 'channels.txt'

The trickiest part of making your own experiment is getting the directories setup correctly and defining them correctly in 'calc.py'. Follow the example of existing experiments for guidance!

##########################

CLEANING UP YOUR MESS

At the "Experiment" direcory level, run 

python clean.py

to remove all sensitivityTable.txt, .jpg, and temp '~' files. If you want to change what's removed by this script,
you can edit the targets in the script's source code.
