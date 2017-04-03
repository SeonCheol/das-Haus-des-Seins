import pyaudio
from pyAudioAnalysis import audioFeatureExtraction as af
import sys
import numpy as np
from math import *


def normalize(data, mean, std):
    normalized = data - mean
    normalized = normalized * 1.0  /std

    return normalized




if __name__ == "__main__":
    CHUNK = 2048
    MIC_NUM = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16
    RECORD_SECONDS = 500

    sum_energy = 0
    idx = 0
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)
    n = int((RATE / CHUNK) * RECORD_SECONDS)
    file = open("data/energyMic1Result.data", "r")
    t = file.readlines()
    t = t[0].split(" ")
    t = map(float, t)
    file.close()

    for i in range(0, n):
        data = stream.read(CHUNK)
        data = np.fromstring(data, dtype='int16')
        fft_data1 = np.fft.fft(data)
        fft_data1 = abs(fft_data1) / (len(fft_data1)/2)
        sum = np.sum(fft_data1)
        if t[0] + t[1]*2< sum:
            print "sum  ==============================", normalize(sum, t[0], t[1])
    file.close()
