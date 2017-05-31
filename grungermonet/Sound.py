import matplotlib.pyplot as plt
import pyaudio
import numpy as np
import queue
import math

RATE = 44100
CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
desiredChunk = 2**12
soundData = queue.Queue(4)

class MyAudio(object):
    def __init__(self):
        self.fft_data = 0
        self.x = [RATE/desiredChunk*1.0]
        for i in range(0, int(desiredChunk/2) -2):
            self.x.append(self.x[i] + RATE/desiredChunk)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)##, stream_callback=self.callback)
        print("recording...")
        ##self.stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        global soundData
        soundData.put(in_data)
        return (None, pyaudio.paContinue)

    def update(self):
        global soundData
        soundData.put(self.stream.read(CHUNK))
        if soundData.full():
            alldata = soundData.get()
            while(soundData._qsize() > 0) :
                alldata = alldata + soundData.get()
            alldata = np.fromstring(alldata, dtype=np.int16)
            self.fft_data = np.fft.fft(alldata)
            self.fft_data = np.abs(self.fft_data)[1:int(desiredChunk/2)]
            print(" freq : ", self.maxFreq())

    def maxFreq(self):
        per_idx = self.x[0]
        # startPoint = int(80 / per_idx) - 1
        # endPoint = int(310 / per_idx) - 1
        i = np.argmax(abs(self.fft_data))
        return self.x[i]

    def deviation(self, Low_cutoff=60, High_cutoff=340):
        M = self.fft_data.size
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, RATE])
        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
        return math.sqrt(np.var(self.fft_data[int(Low_point):int(High_point)]))


    def getFeature(self):
        maxFrq = self.maxFreq()
        devi = self.deviation()
        return np.array([maxFrq, devi])