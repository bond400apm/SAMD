#!/bin/bash
rm ./Output_Charge_Intergral2.txt

duration=100
already_done() { for ((done=0; done<$elapsed; done++)); do printf "▇"; done }
percentage() { printf "| %s%%" $(( (($elapsed)*100)/($duration)*100/100 )); }
clean_line() { printf "\r"; }

elapsed=0
for FILE in ./wavedata/top*; do
	rm wave1.txt
	cp $FILE ./wave1.txt
	python3 WaveReader.py --Alignment >> Output_Charge_Intergral2.txt
	already_done; percentage
	clean_line
	let elapsed=$elapsed+1

done
