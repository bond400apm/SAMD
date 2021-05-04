quick_start = input("Are you using default step size?(Y/N): ")
Mirror_start = float(input("Please tell me your initial mirror position(in degree): "))
Pitch_start = float(input("Please tell me your initial pitch stage position(in mm): "))
if quick_start:
    Mirror_step = 0.02
    Pitch_step = 0.01
else:
    Mirror_step = float(input("Please tell me the jog step size of your mirror(typically 0.02): "))
    Pitch_step = float(input("Please tell me your initial pitch stage position(typically 0.01): "))
Maxpo_number = int(input("Almost there! Now give me the 2 digit position value that maximize the top intensity: "))

Mirrorpo = Maxpo_number//10
Pitchpo = Maxpo_number%10

Mirror = str(Mirror_start + Mirrorpo*Mirror_step) + "°"
Pitch = str(round(Pitch_start + Pitchpo*Pitch_step, 2)) + "mm"

print("The magic happens at({},{})".format(Mirror,Pitch))


