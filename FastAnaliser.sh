#!/bin/bash
#rm ./Output_Charge_Intergral.txt
for FILE in ./wavedata/top*; do
	rm wave1.txt
	cp $FILE ./wave1.txt
	python3 WaveReader.py --Alignment >> Output_Charge_Intergral2.txt

done

