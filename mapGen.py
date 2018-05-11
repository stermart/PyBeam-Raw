#!/usr/bin/python

import pickle as pkl
import pybeam
import pyaudio as pa
import wave

X = pybeam.get_source_matrix(dim=(14,1), delta=(0.02,0))
print(X, flush=True)

p = pa.PyAudio()
speakers = {}

for i in range(p.get_device_count()):
    curr = p.get_device_info_by_index(i)
    if "USB Audio Device" in curr['name'] and curr['maxOutputChannels'] > 0 and curr['name'] not in speakers:
        speakers[curr['name']] = curr['index']

print(speakers, flush=True)

mapping = {}

for speaker in speakers:
    while True:
        wavfile = wave.open('speakertest.wav', 'rb')
        stream = p.open(
            format=p.get_format_from_width(wavfile.getsampwidth()),
            channels=wavfile.getnchannels(),
            rate=wavfile.getframerate(),
            output=True,
            output_device_index=speakers[speaker])

        print("Playing to {}".format(speaker))
        data = wavfile.readframes(1024)
        while not len(data) == 0:
            stream.write(data)
            data = wavfile.readframes(1024)
        stream.close()
    
        try:
            speaker_num = int(input("Which speaker played? (\"R\" to replay)"))
        except:
            print("Replaying {}".format(speaker))
            continue
    

        if speaker_num < 0 or speaker_num >= len(speakers):
            print("Replaying {}".format(speaker))
            continue

        mapping[speaker_num] = speakers[speaker]
        print(mapping)
        break

pkl.dump(mapping, open('mastermap.pkl', 'wb'))

