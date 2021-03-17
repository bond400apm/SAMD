# ---- the trigger height of noise
edge_trigger = -50
# window length of finding Pulse edge
window_length = 5
# Pulse height trigger
Pulse_height = 500
class PulseIdentifier():
    def __init__(self,waveform):
        self.waveform = waveform
        self.lenwavef = len(waveform)
        self.derivative = []
        self.ped_index = []
        self.PulseStart = 70
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
        return pedestal

    def FindPulseStart(self):
        wave_window = []
        derivative_window = []
        IsPulse = False
        time = 0
        while IsPulse == False and time < 250:
            wave_window[:] = [self.waveform[i] for i in range(time,time+window_length)]
            derivative_window[:] = [self.derivative[j] for j in range(time,time+window_length)]
            if abs(wave_window[window_length-1] - wave_window[0]) > Pulse_height and derivative_window[0]<0:
                IsPulse = True
            else:
                IsPusle = False
                time = time + 1
        if time >= 150:
            self.data_valid = False
        self.PulseStart = time
        return time
    def FindPulseEnd(self):
        wave_window = []
        derivative_window = []
        IsPulse = True
        time = self.PulseStart+window_length
        while IsPulse == True:
            wave_window[:] = [self.waveform[i] for i in range(time-window_length+1,time+1)]
            derivative_window[:] = [self.derivative[j] for j in range(time-window_length+1,time+1)]
            if (wave_window[window_length-1] - self.Pedstal) < abs(edge_trigger) and derivative_window[-1]>0:
                IsPulse = False
            else:
                IsPusle = True
                time = time + 1
        self.PulseEnd = time
        return time
    def Process(self,start_b,end_b):
        self.Finderiv()
        self.Pedstal = self.Findped(start_b,end_b)
        start = self.FindPulseStart()
        end = self.FindPulseEnd()
        print("Pedstal = ",self.Pedstal)
        print("start = {}, end = {}".format(start,end))









