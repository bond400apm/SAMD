import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit

def linfunc(x,a,b):
    return a*x + b

f = open("Toplincheck.txt")
#f = open("/home/samd/Documents/linearitycheck.txt","r")
Data = np.genfromtxt(f)
Top_Intensity = abs(Data[:,1])
OD = pow(10,-1*Data[:,0])
Bot_Intensity = abs(Data[:,2])

run_number = int(input("Tell me which run do you want: "))
run_length = 6
startp = run_length*run_number
Processing_top_intensity = Top_Intensity[startp:startp+run_length]
Processing_bot_intensity = Bot_Intensity[startp:startp+run_length]
Processing_OD = OD[startp:startp+run_length]
x = Processing_OD

popt, _ = curve_fit(linfunc,x,Processing_top_intensity)
print("a = {}, b = {}".format(popt[0],popt[1]))
dummy_x = np.linspace(0,0.00012,100)
dummy_y = linfunc(dummy_x,*popt)

plt.xlabel('10^(-OD)')
plt.ylabel('intensity')
plt.plot(x,Processing_bot_intensity,'--rs')
plt.plot(x,Processing_top_intensity,'--b^')
plt.plot(dummy_x,dummy_y)
plt.show()

