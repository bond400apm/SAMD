#!/bin/bash
read -p 'Pressure: ' prevar
read -p 'Run number: ' rint
cp /home/samd/Downloads/wavedump-3.10.0/wave0.txt /home/samd/Downloads/SAMDdata/r${rint}_pres${prevar}wave0.txt
cp /home/samd/Downloads/wavedump-3.10.0/wave1.txt /home/samd/Downloads/SAMDdata/r${rint}_pres${prevar}wave1.txt
