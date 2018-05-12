import numpy as np
from scipy.io import wavfile
import pyaudio as pa
from time import sleep
import os
import shutil
import matplotlib
import pickle as pkl
matplotlib.use('Agg')
import matplotlib.pyplot as plt


p = pa.PyAudio()
stream = p.open(format=pa.paInt16, 
    channels=1, 
    rate=44100, 
    input=True, 
    frames_per_buffer=1024,
    input_device_index=2)


if os.path.exists('soundMeasureResults'):
    shutil.rmtree('soundMeasureResults')
os.mkdir('soundMeasureResults')

for i in range(100):
    input("hit enter for 1 second sample (#{:d}):".format(i+1))
    data = stream.read(44100, exception_on_overflow=False)
    sample = np.fromstring(data, dtype='int16')
    sample = sample.astype('int32')

    #print(sample.shape)
    print("Peak-to-peak: {:d}".format(np.amax(sample) - np.amin(sample)), flush=True)
    print("RMS: {:.2f}".format(np.sqrt(np.average(sample ** 2))))
    pkl.dump(sample, open('soundMeasureResults/{:d}.pkl'.format(i), 'wb'))
    np.savetxt('soundMeasureResults/{:d}.csv'.format(i), sample, delimiter=',', fmt='%d')
    wavfile.write('soundMeasureResults/{:d}.wav'.format(i), 44100, sample.astype('int16'))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(np.linspace(0, 44099, num=44100), sample, 'g-')
    fig.savefig("soundMeasureResults/{:d}.png".format(i))
    plt.close(fig)
    
    #sleep(1)

