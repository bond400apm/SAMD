import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import waveidentifier as wi
from scipy.stats import norm
from scipy.optimize import curve_fit
import argparse
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Instantiate the parser
parser = argparse.ArgumentParser()
# Optional argument
parser.add_argument('--Alignment',action='store_true',help='Use Alignment method')
args = parser.parse_args()
#---- Define a Gaussian function
def Gaussian(x, Amp1, mu1, sigma1):
    return Amp1*np.exp(-1.0*(x-mu1)**2/(2*sigma1**2))

#---- Length of waveform
LenWaveform = 300

#---- Inputs for pedestal calculation
Start_Baseline = 1
End_Baseline   = 50

#---- Pulse information
Number_Of_Pulses  = 7000
Pulse_List_Bottom = []
Pulse_List_Top    = []

Time = [i for i in range(1,LenWaveform+1)]

#---- Read wave files to lists
with open("wave0.txt") as file:
    Waveform_Bottom_PMT = [int(line.strip()) for line in file]
    
with open("wave1.txt") as file:
    Waveform_Top_PMT = [int(line.strip()) for line in file]

Iterator = 0
pulse = 0
invalid_pulse_number = 0
#---- Iterate over the number of pulses given
while pulse < Number_Of_Pulses and Iterator < len(Waveform_Bottom_PMT)/LenWaveform:

    #---- Temporary lists for each pulse
    Processing_Waveform_Top    = []
    Pedestal_List_Top          = []
    Processing_Waveform_Bottom = []
    Pedestal_List_Bottom       = []

    #---- Fill each waveform and pedestal list
    for i in range(LenWaveform):
        Processing_Waveform_Bottom.append(Waveform_Bottom_PMT[i+LenWaveform*Iterator])
        Processing_Waveform_Top.append(Waveform_Top_PMT[i+LenWaveform*Iterator])

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
    Total_Integral_Bottom = 0
    Total_Integral_Top = 0
#    if Bottom.data_valid and Top.data_valid:
    if Bottom.data_valid:
        #---- Integrate the pulse
#        for i in range(Top.PulseStart,Top.PulseEnd):
        for i in range(100,151):
            Total_Integral_Top += Processing_Waveform_Top[i]
        for i in range(100,151):
#        for i in range(Bottom.PulseStart,Bottom.PulseEnd):
            Total_Integral_Bottom += Processing_Waveform_Bottom[i]
    else:
        invalid_pulse_number += 1



#    print(Total_Integral_Top)
    if (Total_Integral_Bottom < -2000):
#    if (Total_Integral_Bottom < -2000 and Total_Integral_Top < -2000):
        Pulse_List_Bottom.append(Total_Integral_Bottom)
        Pulse_List_Top.append(Total_Integral_Top)
        pulse += 1

    Iterator += 1
    
#---- Find I/I_0 for all the pulses
if args.Alignment == False:
    pressure = float(input("tell me what is the pressure:"))
    if len(Pulse_List_Top)>(Number_Of_Pulses/10):
        Ratio = [i/j for i,j in zip(Pulse_List_Top, Pulse_List_Bottom)]
        actual_mean = sum(Ratio)/len(Ratio)
        data_dev = [(R-actual_mean)*(R-actual_mean) for R in Ratio]
        actual_std = np.sqrt(sum(data_dev)/len(data_dev))
        #Create Fit bins
        fit_x = np.linspace(0,3,100)
        #---- Fit I/I_0
        fit_entries, fit_bins = np.histogram(Ratio,bins=fit_x)
        binscenters = np.array([0.5 * (fit_x[i] + fit_x[i+1]) for i in range(len(fit_x)-1)])
        popt, pcov = curve_fit(Gaussian, xdata=binscenters, ydata=fit_entries)
        #print("Fit_Mean = {}, Fit_Std = {}".format(popt[1],abs(popt[2])))
        print("Actual mean = {}, Actual std = {}".format(actual_mean,actual_std))
        print("BotPMT{}:".format(sum(Pulse_List_Bottom)/len(Pulse_List_Bottom)))
        print("TopPMT{}:".format(sum(Pulse_List_Top)/len(Pulse_List_Top)))
        print(max(Ratio))
        plt.hist(Ratio,bins=100)
        plt.xlabel('I/I${_0}$')
        plt.ylabel('Total Per Bin(A.U.)')
        y = Gaussian(binscenters,popt[0],popt[1],abs(popt[2]))
        plt.plot(binscenters, y/7)
        plt.show()
        Bot = sum(Pulse_List_Bottom)/len(Pulse_List_Bottom)        
        Top = sum(Pulse_List_Top)/len(Pulse_List_Top)
       	file1 = open("0604data_v2.txt", "a")
        file1.write(str(current_time)+" "+str(pressure)+" "+str(actual_mean)+" "+str(Bot))
       # file1.write(str(current_time)+" "+str(Bot)+" "+str(Top))
        file1.write("\n")
       # file1.close()


    else:
        print("Not Enough data")
else:
    Ratio = [i/j for i,j in zip(Pulse_List_Top, Pulse_List_Bottom)]
    if len(Pulse_List_Top)>(Number_Of_Pulses/10):
        print('{} {} {}'.format(sum(Ratio)/len(Ratio),sum(Pulse_List_Top)/len(Pulse_List_Top),sum(Pulse_List_Bottom)/len(Pulse_List_Bottom)))
    else:
        print("0 0 0")
       # print("invalid Pulse number = {}".format(invalid_pulse_number))

