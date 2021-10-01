import matplotlib.pyplot as plt
import random
# ---- the trigger height of noise
edge_trigger = -20
# window length of finding Pulse edge
window_length = 5
# Pulse height trigger
Pulse_height = 200
class PulseIdentifier():
    def __init__(self,waveform):
        self.waveform = waveform
        self.lenwavef = len(waveform)
        self.derivative = []
        self.ped_index = []
        self.PulseStart = 20
        self.PulseEnd = 0
        self.Pedstal = 0
        self.data_valid = True
    # ---- Find the derivate of the waveform
    def Finderiv(self):
        num_pre = 0
        adc_pre = 0
        for num,adc in enumerate(self.waveform):
            if num == 0:
                self.derivative.append(0)
            if num > 0:
                slope = (adc-adc_pre)/(num-num_pre)
                self.derivative.append(slope)

            num_pre = num
            adc_pre = adc

    def Findped(self,start_b,end_b):
        ped = []
        for i in range(start_b,end_b-1):
            if abs(self.derivative[i])<abs(edge_trigger) and abs(self.derivative[i+1])<abs(edge_trigger):
                self.ped_index.append(i)
        ped[:] = [self.waveform[i] for i in self.ped_index]
        pedestal = sum(ped)/len(ped)
        self.Pedstal = pedestal

    def FindPulseStart(self):
        wave_window = []
        derivative_window = []
        IsPulse = False
        time = 0
        while IsPulse == False and time < 280:
            wave_window[:] = [self.waveform[i] for i in range(time,time+window_length)]
            derivative_window[:] = [self.derivative[j] for j in range(time,time+window_length)]
            if abs(wave_window[window_length-1] - wave_window[0]) > Pulse_height and derivative_window[0]<0:
                IsPulse = True
            else:
                IsPusle = False
                time = time + 1
        if time >= 250 or time <= 70:
            self.data_valid = False
        self.PulseStart = time
        return time
    def FindPulseEnd(self):
        wave_window = []
        derivative_window = []
        IsPulse = True
        time = self.PulseStart+window_length
        while IsPulse == True and time<299:
            if abs(self.waveform[time] - self.Pedstal) < abs(edge_trigger):
                IsPulse = False
            else:
                IsPusle = True
                time = time + 1
        self.PulseEnd = time
        if time>299:
            self.data_valid = False
        return time
    def Process(self,start_b,end_b):
        self.Finderiv()
        self.Findped(start_b,end_b)
        start = self.FindPulseStart()
        if self.data_valid:
            end = self.FindPulseEnd()
        else:
            self.end = 300
if __name__ == "__main__":
    #---- Length of waveform
    LenWaveform = 300

    #---- Inputs for pedestal calculation
    Start_Baseline = 1
    End_Baseline   = 50

    #---- Pulse information
    Number_Of_Pulses  = 7000
    Processing_Waveform = []
    with open("wave1.txt") as file:
        Waveform_Bottom_PMT = [int(line.strip()) for line in file]
    Pulse_id = random.randint(1,Number_Of_Pulses)
    for i in range(LenWaveform):
        Processing_Waveform.append(Waveform_Bottom_PMT[i+LenWaveform*Pulse_id])
    Test_Pulse = PulseIdentifier(Processing_Waveform)
    Test_Pulse.Process(250,300)
    if Test_Pulse.data_valid:
        Real_Pulse = [Test_Pulse.Pedstal - Processing_Waveform[i] for i in range(Test_Pulse.PulseStart,Test_Pulse.PulseEnd)]
    else:
        print("Pulse is not valid")

    plt.ylabel('Modified Pulse')
    x = range(Test_Pulse.PulseStart,Test_Pulse.PulseEnd)
    y = Real_Pulse
    plt.plot(x,y)
    plt.show()










