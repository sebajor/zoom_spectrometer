import numpy as np
import matplotlib.pyplot as plt
import corr
import struct
from spect_funct import plot_spect
from corr_funct import plot_corr
import time
from meas import meas, vv_meas, vv_meas2

def freq_dds(fpga, freq):
    """Freq in MHz
    """
    fpga.write_int('phase_val',0)
    phase = int(freq/135.*2**24)
    fpga.write_int('phase_data',phase)
    fpga.write_int('phase_val',1)
    
    
    


IP = '192.168.0.40'
bof = 'vector_voltmeter.bof.gz'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(2)

fpga.write_int('rst',1)

freq_dds(fpga, 44.8505)
fpga.write_int('rst',0)

plot_spect(fpga)

#plot_corr(fpga)






