import numpy as np
import pyaudio as pa
from time import sleep
import matplotlib.pyplot as plt


p = pa.PyAudio()
stream = p.open(format=pa.paInt16, 
    channels=1, 
    rate=44100, 
    input=True, 
    frames_per_buffer=1024)

#for i in range(15):
while True:
    data = stream.read(44100)
    sample = np.fromstring(data, dtype='int16')
    sample = sample.astype('int_')
    #print(sample.shape)
    print("Peak-to-peak: {:d}".format(np.amax(sample) - np.amin(sample)), flush=True)
    #plt.plot(np.linspace(0, 44099, num=44100), sample, 'g-')
    #plt.show()
    #sleep(1)

