#!/bin/bash
rm ./Output_Charge_Intergral.txt
for FILE in ./wavedata/top*; do
	rm wave1.txt
	cp $FILE ./wave1.txt
	(echo $FILE && echo " " && python3 WaveReader.py --Alignment && echo "") >> Output_Charge_Intergral.txt

done

