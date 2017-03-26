import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.fftpack as sf

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
#
#Fs = 150.0;  # sampling rate
#Ts = 1.0/Fs; # sampling interval
 # time vector

#ff = 5;   # frequency of the signal
#y = np.sin(2*np.pi*ff*t)



def maxFrequency(X, F_sample, frq, Low_cutoff=80, High_cutoff=300):
    """ Searching presence of frequencies on a real signal using FFT
    Inputs
    =======
    X: 1-D numpy array, the real time domain audio signal (single channel time series)
    Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
    High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
    F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
    """

    M = X.size  # let M be the length of the time series
    Spectrum = np.fft.fft(X)
    [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
    # Convert cutoff frequencies into points on spectrum
    [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
    Low_point = int(Low_point)
    High_point = int(High_point)
    print Low_point, High_point,   frq[Low_point], frq[High_point]
    maximumFrequency = np.where(
        Spectrum == np.max(Spectrum[Low_point: High_point]))  # Calculating which frequency has max power.
    return maximumFrequency

def maxFrequencyForFFT( Spectrum,  F_sample, Low_cutoff=80, High_cutoff=300):
        """ Searching presence of frequencies on a real signal using FFT
        Inputs
        =======
        X: 1-D numpy array, the real time domain audio signal (single channel time series)
        Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
        High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
        F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
        """
        M = Spectrum.size
        print M
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
        print Low_point, High_point
        n = len(Spectrum)  # length of the signal
        k = np.arange(n)
        T = n / F_sample*1.0
        frq = k / T * 1.0  # two sides frequency range
        frq = frq[range(int(n / 2))]  # one side frequency range
        lowIdx = np.searchsorted(frq, 80)
        highIdx = np.searchsorted(frq,300)
        # print k, T,frq,  Low_point, High_point, frq[Low_point], frq[High_point],


        idx = 0
        maxVal = 0
        Spectrum.T[0] = abs(Spectrum.T[0])

        for i in range(len(Spectrum.T[0])):
            if maxVal < abs(Spectrum.T[0][i]):
                maxVal = Spectrum.T[0][i]
                idx = i

        # maximumFrequency = np.where(
        #     Spectrum == np.max(Spectrum[lowIdx:highIdx]))[0]  # Calculating which frequency has max power.
        maximumFrequency = np.argmax(Spectrum[lowIdx: highIdx])
        print maximumFrequency, lowIdx, highIdx, frq[lowIdx], frq[highIdx], frq[idx], idx

        return frq[maximumFrequency], maximumFrequency




fs, data = wavfile.read('sound/realtime_test.wav')
t = np.arange(0,len(data)*1.0/fs,1.0/fs)
y = data
n = len(y) # length of the signal
k = np.arange(n)
T = n/fs
frq = k/T # two sides frequency range
frq = frq[range(int(n/2))] # one side frequency range
# max = maxFrequency(data, fs, frq)
print "??", data.size

# Y = sf.rfft(y) # fft computing and normalization
Y =sf.rfft(y)
Y = Y[range(int(n/2))]
Y= abs(Y)
k = np.argmax(Y)
# dB = round(abs(Y[4018])/abs(Y[k]), 3)
maxFrq, maxFreqIdx = maxFrequencyForFFT(Y, fs)


# print dB, k
# dB = 20 * math.log10(dB)
print  maxFrq, maxFreqIdx

fig, ax = plt.subplots(2, 1)
ax[0].plot(t,y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
ax[1].set_xlim(0,500)
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.show()

