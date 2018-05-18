#!/usr/bin/python

import pybeam
import pickle as pkl
import numpy as np

Y = pybeam.get_source_matrix(dim=(16,1), delta=(0.02,0))
print('source', Y, flush=True)

X = pybeam.get_verification_matrix(R=3, dim=(37,1), b=(90,90))
print('verification', X, flush=True)

sig, samp_freq, dtype = pybeam.read_wav_file('btest8.wav')
print('signal', sig, samp_freq, dtype, sep='\n', flush=True)

Q = pybeam.get_PM_filters(X=X, Y=Y, 
    E_max=pybeam.get_max_energy(R=3, sigma=75, Y=Y),
    p_hat=pybeam.get_target_sound_pressures(X=X, onval=1),
    verbose=True
)
#Q = pybeam.get_DAS_filters(X=X, Y=Y)
#print(Q.shape)
#print(Q)
#Q = np.asmatrix(np.ones(Q.shape, dtype="complex_"))
#print(Q.shape)
print('filters', Q, flush=True)

output = pybeam.map_filters(Q, sig)
print('output', output, flush=True)

mapping = pkl.load(open('mastermap.pkl', 'rb'))
print('mapping', mapping, flush=True)

print('writing wav dir', flush=True)
pybeam.write_wav_dir('bform_out8PM', output, mapping, samp_freq)

print('Plotting Visualization', flush=True)
pybeam.visualize(Q, X, Y, onval=1, R=3, test_index=40, dpu=35, verbose=True)





