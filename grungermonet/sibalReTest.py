from math import *
from pyAudioAnalysis import audioFeatureExtraction as af
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pyaudio
CHUNK = 1024
MIC_NUM = 1
fs = 44100
FORMAT =pyaudio.paInt16
RECORD_SECONDS = 120



def maxFrequency(Spectrum, F_sample, M, Low_cutoff=80, High_cutoff=300):
    """ Searching presence of frequencies on a real signal using FFT
    Inputs
    =======
    X: 1-D numpy array, the real time domain audio signal (single channel time series)
    Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
    High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
    F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
    """

    [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])

    # Convert cutoff frequencies into points on spectrum
    [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])

    maximumFrequency = np.where(
        Spectrum == np.max(Spectrum[int(Low_point): int(High_point)]))  # Calculating which frequency has max power.

    return maximumFrequency


########################
def maxFreq(fftData, RATE, chunk, fftfrq):
    lowPoint =  95
    highPoint = 300
    sum = 0
    frqSum = 0

    lowIdx = np.searchsorted(fftfrq, lowPoint)
    highIdx = np.searchsorted(fftfrq, highPoint)
    # print(lowIdx, highIdx, fftfrq[lowIdx], fftfrq[highIdx])
    # lowIdx = int(chunk*1.0/RATE * lowPoint)
    # highIdx = int(chunk*1.0/RATE * highPoint)
    tmp = fftData[lowIdx:highIdx]
    # which = fftData[lowIdx:highIdx].argmax() + 1
    # # which = tmp.argmax()+1
    # thefreq = 0.0
    # if which != len(fftData) - 1:
    #     y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
    #     x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
    #     # find the frequency and output it
    #     thefreq = (which + x1) * RATE / chunk
    #     # print "The freq is %f Hz." % (thefreq)
    # else:
    #     thefreq = which * RATE / chunk
    #     # print "The freq is %f Hz." % (thefreq)
    maxIdx = tmp.argmax()
    for i in range(maxIdx-1, maxIdx+1):
        frqSum += fftfrq[i+lowIdx] * int(tmp[i])
        sum += int(tmp[i])
    thefreq = frqSum*1.0 / sum
    #thefreq = fftfrq[maxIdx+lowIdx]
    return thefreq



######################
def dataAnal():
    floatData = []
    idx = 0
    f = open("data/voiceEnergy.data")
    line = f.readlines()
    datas = line[0].split(" ")
    for i in range(len(datas)):
        try:
            tmp = float(datas[i])
            if tmp > 15:
                floatData.append(tmp)
                idx += 1
        except Exception as e:
            print e.message
            continue
    mean = np.mean(floatData)
    var = np.var(floatData)
    f.close()

    f = open("data/voiceEnergyResult.data", "w+")
    f.write(str(mean) + " " + str(sqrt(var)))
    f.close()

if __name__== "__main__":
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=MIC_NUM,
                            rate=fs, input=True, frames_per_buffer=CHUNK)

    t = np.arange(0, CHUNK*1.0/fs,1.0/fs)
    n = int( ( fs / CHUNK) * RECORD_SECONDS)

    plt.ion()
    fig, ax = plt.subplots(2, 1)
    # file = open("data/voiceEnergy.data", "a")

    f = open("data/voiceEnergyResult.data", "r")
    energyAnal = f.readline().split(" ")
    f.close()
    for i in range(0, n/2):
        # plt.hold(True)
        y = stream.read(CHUNK*2)
        n = len(y) # length of the signal
        fftfrq = np.fft.fftfreq(n, d=1.0/fs)
        fftfrq = fftfrq[range(int(n/2))]
        # k = np.arange(n)
        # T = n*1.0/fs
        # frq = k/T*1.0 # two sides frequency range
        # frq = frq[range(int(n/2))] # one side frequency range
        # max = maxFrequency(data, fs, frq)
        y = np.fromstring(y, dtype='int16')
        Y = np.fft.fft(y) # fft computing and normalization

        # Y = np.fft.fft(y)/n
        Y = abs(Y)
        # max = maxFrequency(Y, fs, y.size)


        # print fftfrq[max]
        plt.cla()

        ax[0].plot(t, y[range(int(len(y)/2))], 'b')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Amplitude')
        ax[0].grid(True)
        plt.cla()
        ax[1].plot(fftfrq, abs(Y), 'r')
        ax[1].set_xlabel('Freq (Hz)')
        ax[1].set_ylabel('|Y(freq)|')
        ax[1].set_xlim(0,500)
        # ax[1].vlines(frq, [0], abs(Y))
        ax[1].grid(True)
        plt.draw()
        plt.pause(0.00001)
        plt.cla()
        ene = af.stEnergy(y)
        # if float(energyAnal[0])< ene:
        #     max = maxFreq(Y, fs, y.size, fftfrq)
        #     print("talk!!")
        #     print(max), ene

        #else: print("____________________-----------")
        # file.write(str(abs(ene)) + " ")
    # file.close()

    stream.close()
    p.terminate()

    # dataAnal()



