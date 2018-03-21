import numpy as np
import scipy.signal
import scipy.io.wavfile

__c = 343 #speed of sound
__l2 = lambda arr: np.sqrt(np.sum(arr**2))
__Zf = lambda x_m, y_l, omega: np.e**(-1j * omega / __c * __l2(x_m - y_l)) / (4 * np.pi * l2(x_m - y_l))

def get_source_matrix(dim=(2, 1), delta=(0.02, 0), center=(0, 0, 0)):
    L = dim[0] * dim[1]
    y = np.zeros((L, 3))
    for x in range(dim[0]):
        for z in range(dim[1]):
            y[x * dim[1] + z] = np.array([center[0] + (x-dim[0]//2+0.5)*delta[0],
                                    center[1],
                                    center[2] + (z-dim[1]//2+0.5)*delta[1]])
    return y

def get_verification_matrix(R=3, dim=(37,1), b=(90,90)):
    M = dim[0] * dim[1]
    delta_theta = 180 / (dim[0] - 1) * np.pi / 180 if dim[0] > 1 else 0 
    delta_phi = 180 / (dim[1] - 1) * np.pi / 180 if dim[1] > 1 else 0
    xtmp = np.zeros((M, 3))
    bidx, mindist, targpoint = -1, 
        float('inf'), 
        np.array([R*np.sin(np.radians(b[1]))*np.cos(np.radians(b[0])),
            R*np.sin(np.radians(b[1]))*np.sin(np.radians(b[0])),
            R*np.cos(np.radians(b[1]))])
    print(targpoint)
    if dim[0] <= 1: #semicircle with variable phi
        for j in range(dim[1]):
            xtmp[j] = np.array([0, R*np.sin(j*delta_phi), R*np.cos(j*delta_phi)])
            if __l2(xtmp[j] - targpoint) < mindist:
                bidx = j
                mindist = __l2(xtmp[j] - targpoint)
    elif dim[1] <= 1: #semicircle with variable theta
        for i in range(dim[0]):
            xtmp[i] = np.array([R*np.cos(i*delta_theta), R*np.sin(i*delta_theta), 0])
            if __l2(xtmp[i] - targpoint) < mindist:
                bidx = i
                mindist = __l2(xtmp[i] - targpoint)
    else: #full hemisphere
        for i in range(dim[0]):
            for j in range(dim[1]):
                idx = i * dim[1] + j
                xtmp[idx] = np.array([R*np.cos(i*delta_theta)*np.sin(j*delta_phi),
                                R*np.sin(i*delta_theta)*np.sin(j*delta_phi),
                                R*np.cos(j*delta_phi)])
                if __l2(xtmp[idx] - targpoint) < mindist:
                    bidx = idx
                    mindist = __l2(xtmp[idx] - targpoint)
    x = xtmp.copy()
    x[0], x[1:bidx+1] = xtmp[bidx], xtmp[:bidx]
    return x

if __name__ == '__main__':
    print(get_source_matrix())
    print(get_verification_matrix())
            
    
    
  
