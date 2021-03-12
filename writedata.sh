#!/bin/bash
read -p 'Pressure: ' prevar
read -p 'Run number: ' rint
cp wave0.txt /home/samd/Downloads/SAMDdata/r${rint}_pres${prevar}wave0.txt
cp wave1.txt /home/samd/Downloads/SAMDdata/r${rint}_pres${prevar}wave1.txt
