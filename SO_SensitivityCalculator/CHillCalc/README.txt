##########################

'CHillCalc' was  written in full by Charles Hill at UC Berkeley
Publish date = 2016-12-07
Latest revision = 2.0
Latest revision date = 2017-01-29

##########################

REVISION HISTORY

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
    -- 'atmosphere.txt' contains the atmosphere spectrum
    -- 'calc.py' calculates sensitivity for all optical designs associated with this experiment
    -- 'optimizeFP.py' calculates the mapping-speed vs pixel size curve for all optical designs associated with this experiment
(2) Experimental Designs (i.e. SO V1 configurations)
(3) Telescopes (for SO, there is only one telescope in v3.0 of this code, but we will likely add more soon)
    -- 'experiment.txt' contains parameters that are same for all telescopes
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

-- OpticalCouplingToFP = an overall factor for how well the focal plane couples to the optics
-- Fnumber = detector F/#
-- Bath temperature = base temperature for this telesope's focal plane

##########################

OPTICALCHAIN.TXT

This file contains information about all of the optics within the telescope. In the absence of information, the entry must be 'NA'. Note that this file does not contain information about the sky or the detector channels.

-- Element = optic name
-- Temp = temperature
-- Thick = thickness, used to cacluate absorption
-- Index = index of refraction, used to calculate absorption
-- LossTan = dielectric loss tangent, used to calculate absorption
-- Conductivity = used to calculate mirror absorption
-- Absorb = can specify an absorption, allowing for 'Thick', 'Index', and 'LossTan' to be left blank
-- AbsorbFreq = frequency at which 'Absorb' is true. This is used for scaling the dielectric absorption linearly to other frequencies in the absencd of thickness, index, and lossTan
-- SurfaceRough = RMS surface roughness used to caculate the scattering of the mirror
-- ScattFrac = the fraction of reflected light that is scattered to somewhere other than back to the focal plane
-- ScattTemp = the temperature of the surface upon which the scattered light lands

##########################

CHANNELS.TXT

This file contains information regarding the frequency channels and their detectors. In the absence of information, the entry must be 'NA'.

-- BandID = band name
-- PixelID = name of pixel this band is on
-- BandCenter = central frequency of the frequency band
-- FBW = band fractional bandwidth (fHi - fLo)/BandCenter
-- PixSize = pixel diameter, or equivilantly spacing between pixels on the focal plane
-- NumDet = number of detectors for this frequency channel in this telescope
-- WaistFact = equivalent to 'w_f', which defines the ratio of the pixel diameter to its gaussian beam waist size D/w_0
-- DetEff = detector efficiency, including antenna performance, microstrip loss, impedance mismatch at the load resistor, etc.
-- Psat = saturation power
-- PsatFact = If 'Psat' is 'NA', then Psat = PsatFact*Popt (see below)
-- CarrierIndex = thermal carrier index for bolometer thermal conduction
-- TransTemp = Bolometer transition temperature
-- TcFrac = If 'TransTemp' is 'NA', then Tc = TcFrac*(Bath Temperature)
-- Bunch Factor = a weighting for the Dicke factor in the photon noise term. Default should be 1.0
-- Yield = detector yield for this channel
-- NEI = noise equivalent current for this channel. If 'NA', readout noise contributes only 10% to the total noise
-- nModes = number of modes read out by a detector on this channel. Can become less than 1.0 if the pixel is too small (no formalism here yet)
-- boloR = bolometer resistance (used to calculate readout noise)

##########################

EXECUTABLES

Within each experiment directory, there are the following executables

-- 'calc.py' gathers directories at the design level (i.e. the folder that contains the 'experiment.txt' config file and the telescope directories), creates 'Experiment' and 'Display' objects, calculates experimental sensitivity, and outputs the sensitivity tables both to the terminal and to files called 'sensitivityTable.txt'

-- 'optimizeFP.py' takes directories at the design level, creates 'Experiment', and 'Optimize' objects, and calculates mapping speed as a function of pixel spacing and writes the result to plots

##########################

SETTING THE ENVIRONMENT

Before running any executables, you must set the environment.

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
     -- Within the 'Design/' directory = your design directories (the names of these design directories are used to name the 'Experiment' objects), and a 'calc.py' executable
     	-- Within each of your created design directories = 'experiment.txt' and your telescope directories (the names of these telescope directories are used to name the 'Telescope' objects)
	   -- Within each of your telescope directories = 'camera.txt', 'opticalChain.txt', and 'channels.txt'

The trickiest part of making your own experiment is getting the directories setup correctly and defining them correctly in 'calc.py'. Follow the example of existing experiments for guidance!

##########################
