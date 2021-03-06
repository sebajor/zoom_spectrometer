import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc


def plot_spect(fpga_):
    global fpga, data, freq
    
    fpga = fpga_
    bw = 135
    freq = np.linspace(0, bw, 1024, endpoint=False)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    data1, = ax1.plot([],[], lw=2)
    data2, = ax2.plot([],[], lw=2)
    
    data = [data1, data2]

    ax1.set_title('DDS')
    ax1.set_xlim(0, bw)
    ax1.set_ylim(10, 160)
    ax1.grid()    

    ax2.set_title('DCC')
    ax2.set_xlim(0, bw)
    ax2.set_ylim(10, 160)
    ax2.grid()
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

    



def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data




def get_data():
    dds_data = np.array(struct.unpack('>1024Q', fpga.read('data_dds', 1024*8)))
    ddc_data = np.array(struct.unpack('>1024Q', fpga.read('data_ddc', 1024*8)))
    return [10*np.log10(dds_data+1), 10*np.log10(ddc_data+1)]



def animate(i):
    aux = get_data()
    data[0].set_data(freq, aux[0][::-1])
    data[1].set_data(freq, aux[1])
    return data









