#!/bin/bash

rm Output_Charge_Integral.txt

Scanning_Angle=0
Scanning_Angle_Increment=1
Scanning_Pitch=0
Scanning_Pitch_Increment=1
SECONDS=0
while [ $Scanning_Angle -lt 10 ]; do
    while [ $Scanning_Pitch -lt 10 ]; do

	(echo "s" && sleep 1s && echo "W" && sleep 6s && echo "s" && echo "q") | wavedump
	(echo $Scanning_Angle && echo " " && echo $Scanning_Pitch && python3 WaveReader.py --Alignment && echo "") >> Output_Charge_Integral.txt
	
	let Scanning_Pitch=Scanning_Pitch+$Scanning_Pitch_Increment
	now=$SECONDS
	Pause=$((61-$(($now % 61))))
	sleep $Pause
	
    done

    Scanning_Pitch=0
    let Scanning_Angle=Scanning_Angle+$Scanning_Angle_Increment
    
done    
