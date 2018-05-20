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
import socket
import sys

host = "192.168.1.162"
port = 5007
secs = 20

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))

p = pa.PyAudio()
stream = p.open(format=pa.paInt16, 
    channels=2, 
    rate=44100, 
    input=True, 
    frames_per_buffer=1024,
    input_device_index=2)


if os.path.exists('soundMeasureResults'):
    shutil.rmtree('soundMeasureResults')
os.mkdir('soundMeasureResults')

for i in range(100):
    input("hit enter for 1 second sample (#{:d}):".format(i+1))
    soc.send('PLAYBACK'.encode())
    data = soc.recv(1024).decode()
    print('Data received: {}'.format(data), flush=True) 

    raw_data = stream.read(secs*44100, exception_on_overflow=False)
    print('Done recording!', flush=True)
    data = np.fromstring(raw_data, dtype='int16')
    chunk_length = len(data) // 2
    data = np.reshape(data, (chunk_length, 2))
    data = data.astype('int32')*50
    sample = (data[:, 0] + data[:, 1]) // 2
    print(sample)

    #print(sample.shape)
    print("Peak-to-peak: {:d}".format(np.amax(sample) - np.amin(sample)), flush=True)
    print("RMS: {:.2f}".format(np.sqrt(np.average(sample ** 2))))
    pkl.dump(sample, open('soundMeasureResults/{:d}.pkl'.format(i), 'wb'))
    np.savetxt('soundMeasureResults/{:d}.csv'.format(i), sample, delimiter=',', fmt='%d')
    wavfile.write('soundMeasureResults/{:d}.wav'.format(i), 44100, sample.astype('int16'))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(np.linspace(0, 44100 * secs - 1, num=44100 * secs), sample, 'g-')
    fig.savefig("soundMeasureResults/{:d}.png".format(i))
    plt.close(fig)
    
    #sleep(1)
oi
