#!/usr/bin/python

import pybeam
import pickle as pkl

Y = pybeam.get_source_matrix(dim=(16,1), delta=(0.02,0))
print('source', Y, flush=True)

X = pybeam.get_verification_matrix(R=1, b=(90,90))
print('verification', X, flush=True)

sig, samp_freq, dtype = pybeam.read_wav_file('btest6.wav')
print('signal', sig, samp_freq, dtype, sep='\n', flush=True)

Q = pybeam.get_PM_filters(X=X, Y=Y, 
    E_max=pybeam.get_max_energy(R=1, sigma=25, Y=Y),
    p_hat=pybeam.get_target_sound_pressures(X=X, onval=1),
    verbose=True
)
#Q = pybeam.get_DAS_filters(X=X, Y=Y)
print('filters', Q, flush=True)

output = pybeam.map_filters(Q, sig)
print('output', output, flush=True)

mapping = pkl.load(open('mastermap.pkl', 'rb'))
print('mapping', mapping, flush=True)

print('writing wav dir', flush=True)
pybeam.write_wav_dir('bform_out6PM', output, mapping, samp_freq)





