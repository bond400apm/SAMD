Read this document before doing anything dangerous:

This repo is the full version of SAMD project control and data reading software
============================================================================


WaveReader.py:
option: --Alignment    This option output the average signal intensity read by the top PMT. It is used in Beam_Maximiser.sh file to find the direction that maximize the Top PMT reading.

If no arguement is parsed, this script read the waveform from wave0.txt and wave1.txt and output a histogram of I/I0.

Waveidentifier.py:
This script stores the Class that identifiy the laser pulse within a given waveform. If executed, it test the Wave Identifier Class using a random input from wave0.txt and return the shape of laser pulse.

Beam_Maximiser.sh:
Don't use if digitizer or mechanical stages are off.
This script Automatically analyse data from digitizer every 1 minute while the mechanical stages move to a new position, it returns the Top PMT signal intensity for different. This is used to find the BEST alignment.

Fast_Beam_Maximiser.sh
The same as Beam_Maximiser, only faster. It takes stage rest time in to consideration for high precision. It doesn't analyse the data directly, but store the raw data into wavedata/ directory, which can later be analized. 
For stage step = 0.1 mm, stage rest time is set to 0.54s
