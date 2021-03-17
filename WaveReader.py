import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import waveidentifier as wi
from scipy.stats import norm

#---- Length of waveform
LenWaveform = 300

#---- Inputs for pedestal calculation
Start_Baseline = 250
End_Baseline   = 300

#---- Pulse information
Number_Of_Pulses  = 10
Pulse_List_Bottom = []
Pulse_List_Top    = []

Time = [i for i in range(1,LenWaveform+1)]

#---- Read wave files to lists
with open("wave0.txt") as file:
    Waveform_Bottom_PMT = [int(line.strip()) for line in file]
    
with open("wave1.txt") as file:
    Waveform_Top_PMT = [int(line.strip()) for line in file]

Iterator = 0

#---- Iterate over the number of pulses given
for pulse in range(Number_Of_Pulses):

    #---- Temporary lists for each pulse
    Processing_Waveform_Top    = []
    Pedestal_List_Top          = []
    Processing_Waveform_Bottom = []
    Pedestal_List_Bottom       = []

    #---- Fill each waveform and pedestal list
    for i in range(LenWaveform):
        Processing_Waveform_Bottom.append(Waveform_Bottom_PMT[i+LenWaveform*Iterator])
        Processing_Waveform_Top.append(Waveform_Top_PMT[i+LenWaveform*Iterator])

        if (i >= Start_Baseline and i < End_Baseline):
            Pedestal_List_Bottom.append(Waveform_Bottom_PMT[i])
            Pedestal_List_Top.append(Waveform_Top_PMT[i])
    Bottom = wi.PulseIdentifier(Processing_Waveform_Bottom)
    Top = wi.PulseIdentifier(Processing_Waveform_Top)
    Bottom.Process(Start_Baseline,End_Baseline)
    Top.Process(Start_Baseline,End_Baseline)
    
    #---- Find pedestal and subtract from the waveforms
#    Pedestal_Bottom = sum(Pedestal_List_Bottom)/(End_Baseline - Start_Baseline)
    Pedestal_Bottom = Bottom.Pedstal
    Pedestal_Top = Top.Pedstal
    Processing_Waveform_Bottom[:] = [Processing_Waveform_Bottom - Pedestal_Bottom for Processing_Waveform_Bottom in Processing_Waveform_Bottom]
#    Pedestal_Top = sum(Pedestal_List_Top)/(End_Baseline - Start_Baseline)
    Processing_Waveform_Top[:] = [Processing_Waveform_Top - Pedestal_Top for Processing_Waveform_Top in Processing_Waveform_Top]
    if Bottom.data_valid and Top.data_valid:
        #---- Integrate the pulses
        Total_Integral_Bottom = 0
        Total_Integral_Top    = 0
        for i in range(Top.PulseStart,Top.PulseEnd):
            Total_Integral_Top    += Processing_Waveform_Top[i]
        for i in range(Bottom.PulseStart,Bottom.PulseEnd):
            Total_Integral_Bottom += Processing_Waveform_Bottom[i]



#    print(Total_Integral_Top)

    if (Total_Integral_Bottom < -10000):
        Pulse_List_Bottom.append(Total_Integral_Bottom)
        Pulse_List_Top.append(Total_Integral_Top)

    Iterator += 1
    
#---- Find I/I_0 for all the pulses
Ratio = [i/j for i,j in zip(Pulse_List_Top, Pulse_List_Bottom)]

#---- Fit I/I_0
mean,std=norm.fit(Ratio)
print("Mean:    ",mean,"    Standard Deviation:    ",std)

plt.hist(Ratio,bins=100,density=True)
plt.xlabel('I/I${_0}$')
plt.ylabel('Total Per Bin(A.U.)')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 1000)
y = norm.pdf(x, mean, std)
plt.plot(x, y)
#y = mlab.normpdf(bins, mu, sigma)
plt.show()
#print(Waveform_Bottom_PMT)
