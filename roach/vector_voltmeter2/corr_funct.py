import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc



def plot_corr(fpga_):
    global data, fpga, freq
    fpga = fpga_; 
    
    bw = 135.
    freq = np.linspace(0, bw/128, 1024, endpoint=False)

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(224)
    data1, = ax1.plot([],[], lw=2)
    data2, = ax2.plot([],[], lw=2)
    data3, = ax3.plot([], [], lw=2)
    data = [data1, data2, data3]
    ax1.set_title('Relative angle [rad]')
    ax1.set_xlabel('frequency?')
    ax1.set_ylabel('$\phi$[rad]')
    ax2.set_title('Power ZDOK0  [dB]')
    ax2.set_xlabel('frequency')
    ax2.set_ylabel('[dB]')
    ax3.set_title('Power ZDOK1 [dB]')
    ax3.set_xlabel('frequency')
    ax3.set_ylabel('[dB]')
    ax1.set_xlim(0,bw/128)
    ax1.set_ylim(-180, 180) #modificar el valor de los limites
    ax2.set_xlim(0,bw/128)
    #ax2.set_xlim(0, channels-1)
    ax2.set_ylim(10, 120)
    ax3.set_xlim(0,bw/128)
    #ax3.set_xlim(0, channels-1)
    ax3.set_ylim(10, 120)
    ax1.grid()
    ax2.grid()
    ax3.grid()
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show() 



def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    data[2].set_data([],[])
    #ipdb.set_trace()
    return data

def function():
    helper = '>1024Q'
    A2 = np.array(struct.unpack(helper, fpga.read('cic_spectrum_spect0', 1024*8,0)))
    B2 = np.array(struct.unpack(helper, fpga.read('cic_spectrum_spect1', 1024*8,0)))
    
    raw_ang = struct.unpack('>2048q', fpga.read('cic_spectrum_corr', 1024*16,0))
    
    ang = np.rad2deg(np.arctan2(raw_ang[1::2], raw_ang[::2]))
    log_a = 10*np.log10(A2)
    log_b = 10*np.log10(B2)
    return [ang, log_a, log_b]


def animate(i):
    aux = function()
    data[0].set_data(freq,aux[0])
    data[1].set_data(freq, aux[1])
    data[2].set_data(freq, aux[2])
    
    return data
