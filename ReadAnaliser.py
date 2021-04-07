import matplotlib.pyplot as plt

mirror_range = 0.2
stage_range = 0.2


with open("Output_Charge_Intergral.txt") as file:
    Intensity = [abs(float(line.strip())) for line in file]

x = range(len(Intensity))

plt.xlabel('position')
plt.ylabel('intensity')
plt.plot(x,Intensity)
plt.show()
