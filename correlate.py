import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np
from numpy.linalg.linalg import norm
from scipy.io import wavfile
import pandas
import gcc_phat as gp

fs_for, data_for = wavfile.read('test_stretched_forpos.wav')
fs_back, data_back = wavfile.read('test_stretched_backpos.wav')

if fs_for != fs_back:
    print("sampling is not equal")
    exit(-1)

if len(data_for) != len(data_back):
    print("time is not equal")
    exit(-1)

fs = fs_for
length = len(data_for)

t = np.arange(0, length/fs, 1.0/fs)
signal_for = data_for.T[0]
signal_back = data_back.T[0]

length = len(signal_for)

k = np.arange(length)
T = length/fs

frq = k/T
#frq = frq[range(int(length/2))]

Y_for = np.fft.fft(signal_for)

Y_back = np.fft.fft(signal_back)
###
#fig, ax = plt.subplots(4, 1)
# ax[0].plot(frq, abs(Y_for), 'b')
# ax[0].set_xlabel('Freq (Hz)')
# ax[0].set_ylabel('|Y_for(freq)|')
# ax[1].plot(t,signal_for, 'b')
# ax[1].set_xlabel('Time')
# ax[1].set_ylabel('Amplitude')
#
# ax[2].plot(frq,abs(Y_back),'r') # plotting the spectrum
# ax[2].set_xlabel('Freq (Hz)')
# ax[2].set_ylabel('|Y_back(freq)|')
# ax[3].plot(t, signal_back, 'r')
#ax[3].set_xlabel('Time')
#ax[3].set_ylabel('Amplitude')
#plt.show()

###
gcc_for = gp.xcorr_freq(signal_back[range(int(length/7))], signal_for[range(int(length/7))])

same_corr = np.correlate( Y_back[range(int(length/7))],Y_for[range(int(length/7))], 'full')
same_corr = same_corr/same_corr[np.argmax(same_corr)]

print("gcc phat" )
print(abs(0.5- (np.argmax(gcc_for)/len(gcc_for))))
print("autocor ")
print(abs(0.5- (np.argmax(same_corr)/len(same_corr))))
n = len(same_corr)
sec = np.arange(-n/fs/2, n/fs/2, 1.0/fs)

fig, ax = plt.subplots(2, 1)
ax[0].plot(range(0, len(gcc_for)),gcc_for)
ax[1].plot(sec, same_corr)
plt.show()
print(np.argmax(same_corr))