#!/usr/bin/python

import pybeam

Y = pybeam.get_source_matrix()
print(Y, flush=True)

X = pybeam.get_verification_matrix(b=(45,90))
print(X, flush=True)

sig, samp_freq, dtype = pybeam.read_wav_file('btest.wav')
print(sig, samp_freq, dtype, sep='\n', flush=True)

Q = pybeam.get_DAS_filters(X=X, Y=Y)
print(Q, flush=True)

output = pybeam.map_filters(Q, sig)
print(output, flush=True)

mapping = {0:3}
pybeam.write_wav_dir('ex1', output, mapping, samp_freq)

pybeam.playback_wav_dir('ex1')




