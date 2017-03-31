import pyaudio
from pyAudioAnalysis import audioFeatureExtraction as af
import sys
import numpy as np
from math import *

def analTheTrainingFile():
    file = open("data/energyDataForTrainingMic1.data", "r")
    stream = file.readlines()
    datas = stream[0].split(" ")
    datas = datas[:-1]
    datas = map(float, datas)

    mean = np.mean(datas)
    std = sqrt(np.var(datas))

    file.close()
    f = open("data/energyMic2Result.data", "w+")
    f.write(str(mean) + " " + str(std))
    f.close()




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

    file = open("data/energyDataForTrainingMic1.data", "a")



    for i in range(0, n):
        # if (idx % 10 == 0):
        #     mean = sum_energy * 1.0 / idx
        #     file.write(str(mean))
        #     sum_energy = 0
        #     idx = 0
        data = stream.read(CHUNK)
        data = np.fromstring(data, dtype='int16')
        fft_data1 = np.fft.fft(data)
        fft_data1 = abs(fft_data1) / (len(fft_data1)/2)
        sum = np.sum(fft_data1)
        if t[0] + t[1]*2< sum:
            print "sum  ==============================", sum
        # print(sum, t[0])
        file.write(str(sum) + " ")
    file.close()


