import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np
from scipy.io import wavfile
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
#
#Fs = 150.0;  # sampling rate
#Ts = 1.0/Fs; # sampling interval
 # time vector

#ff = 5;   # frequency of the signal
#y = np.sin(2*np.pi*ff*t)

fs, data = wavfile.read('test.wav')
t = np.arange(0,len(data)/fs,1.0/fs)
y = data.T[0]
n = len(y) # length of the signal
k = np.arange(n)
T = n/fs
frq = k/T # two sides frequency range
frq = frq[range(int(n/2))] # one side frequency range

Y = np.fft.fft(y) # fft computing and normalization
Y = Y[range(int(n/2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(t,y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.show()
