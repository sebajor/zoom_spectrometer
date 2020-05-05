import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc
from scipy.fftpack import fft

def meas(fpga):
    fpga.write_int('rst',1)
    fpga.write_int('rst',0)
    
    A = np.array(struct.unpack('>131072i',fpga.read('cic_spectrum_spect0', 65536*4*2)))
    A = A[::2]+1j*A[1::2]
    
    B = np.array(struct.unpack('>131072i',fpga.read('cic_spectrum_spect1', 65536*4*2)))
    B = B[::2]+1j*B[1::2]
    
    spect0 = fft(A)
    spect1 = fft(B)
    
    correlation = spect0*np.conjugate(spect1)
    ang = np.angle(correlation, deg=True)
    #pow_diff = 20*(np.log10(np.abs(spect0))-np.log10(np.abs(spect1)))
    
    return [ang, spect0, spect1]


def vv_meas(fpga):
    aux = meas(fpga)
    ind = np.argmax(aux[1])
    pow_diff = 20*(np.log10(np.abs(aux[1][ind]))-np.log10(np.abs(aux[2][ind])))
    ang = aux[0][ind]
    return [ang, pow_diff, ind]
    
    
    
def vv_meas2(fpga, ind):
    aux = meas(fpga)
    ind = np.argmax(aux[1])
    pow_diff = 20*(np.log10(np.abs(aux[1][ind]))-np.log10(np.abs(aux[2][ind])))
    ang = aux[0][ind]
    return [ang, pow_diff, ind]




