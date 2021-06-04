import matplotlib.pyplot as plt
import numpy as np

mirror_range = 0.2
stage_range = 0.2

f = open("Output_Charge_Intergral2.txt","r")
Data = np.genfromtxt(f)
Top_Intensity = abs(Data[:,1])
Ratio = Data[:,0]
Bot_Intensity = abs(Data[:,2])

#with open("Output_Charge_Intergral2.txt") as file:
#    Top_Intensity = [abs(float(line.split()[1])) for line in file]
#    Ratio = [abs(float(line.split()[0])) for line in file]
x = range(len(Top_Intensity))
#plt.ylim([30000,62000])
plt.xlabel('position')
plt.ylabel('intensity')
plt.plot(x,Bot_Intensity)
plt.plot(x,Top_Intensity)
for i in range(10):
    plt.axvline(x=i*10)
plt.show()
