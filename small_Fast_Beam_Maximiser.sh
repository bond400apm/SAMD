#!/bin/bash

rm -r wavedata
mkdir ./wavedata/
Scanning_Angle=0
Scanning_Angle_Increment=1
Scanning_Pitch=0
Scanning_Pitch_Increment=1
old=`date +%s%2N`
Stage_time=0.25
while [ $Scanning_Angle -lt 4 ]; do
    while [ $Scanning_Pitch -lt 10 ]; do
	(echo "s" && sleep 1s && echo "W" && sleep 3s && echo "s" && echo "q") | wavedump
	cp wave1.txt ./wavedata/topwave$Scanning_Angle$Scanning_Pitch.txt
	cp wave0.txt ./wavedata/botwave$Scanning_Angle$Scanning_Pitch.txt

	let Scanning_Pitch=Scanning_Pitch+$Scanning_Pitch_Increment
	now=`date +%s%2N`
	Pause=`echo 10-$(($now - $old))/100+$Stage_time | bc -l`
	echo "sleeping for: " && echo $Pause
	sleep $Pause
	old=`date +%s%2N`
	
    done

    Scanning_Pitch=0
    let Scanning_Angle=Scanning_Angle+$Scanning_Angle_Increment
    
done    
