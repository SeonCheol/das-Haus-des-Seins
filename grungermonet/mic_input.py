import numpy as np
import pyaudio
import gcc_phat as gcc
import math

class GrungerMonet:
    CHUNK = 1024
    MIC_NUM = 2
    RATE = 44100
    FORMAT =pyaudio.paInt16
    RECORD_SECONDS = 10

    ## installed mic array's coordinate
    mic_x = []
    mic_y = []


    # the time delayed from another signal
    time_delay = 0

    # signal data from mics
    sig = []
    sig_fft = []

    ## for sound speed
    sound_speed = 0
    temperature = 15

    ## straight distance in the exhibition space
    dist = 3 ## unit is meter
    ## this value indicate how much a index mean distance (?영어가 짧음)
    dist_per_index = 0

    ## display
    width = 2048
    height = 1024


    def __init__(self, dist=3, temperature=15):
        ## initalize the variables
        self.temperature = temperature
        self.dist = dist

        ## calculate sound speed
        self.sound_speed = (273 + self.temperature) / 288
        self.sound_speed = round( self.sound_speed, 5)
        self.sound_speed = 340.3 * math.sqrt(self.sound_speed)

        ## calculate distance what the index means
        max_del_time = self.dist / self.sound_speed
        max_del_time = round(max_del_time, 5)
        self.dist_per_index = round( (1/self.RATE), 5)


        print("start the app")



    def play(self):
        print('playing')
        #### input voice ###
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT, channels=self.CHANNELS,
                rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        n = int( (self.RATE / self.CHUNK) * self.RECORD_SECONDS)
        frames = []

        for i in range(0, n):
            ### input from mic1
            data1 = stream.read(self.CHUNK)
            frames.append(data1)
            data1 = np.fromstring(data1, dtype='int16')
            ### input from mic2
            data2 = data1
            print("for")

        ### get delay time from gcc_PHAT ###
            self.get_delay_time_gcc(data1, data2)
        ### calculate the sound local ###





    def get_delay_time_cor(self, data, fs):
        n = len(data) # number of signal data

        fft_data = []
        for i in range(n):
            tmp_fft = np.fft.fft(self.data[i])
            fft_data.append(tmp_fft)

        # get the correlate and get max value of correlation
        cor = np.correlate(fft_data[0], fft_data[1], 'full')
        max_idx = np.argmax(cor)
        k = len(cor)
        t = np.arange(-k/fs/2, k/fs/2, 1.0/fs)

        delay_time = t[max_idx]
        return delay_time

    def get_delay_time_gcc(self, data1, data2, fs=RATE):
        gcc_result = gcc.xcorr_freq(data1, data2)

        max_idx = np.argmax(gcc_result)
        k = len(gcc_result)
        # t = np.arange(-k / fs / 2, k / fs / 2, 1.0 / fs)

        delay_time = max_idx - (k/2)
        delay_time = delay_time * self.dist_per_index

        return delay_time

    def cal_location(self, delay_time):
        meter_per_dot = round(self.dist / self.width, 5)

        diff_from_cent = meter_per_dot * delay_time
        loc = self.width/2 + diff_from_cent

        return int(loc)


    ## get sound speed
    def sound_speed(self, temperature=15):
        tmp = (273 + temperature) / 288
        tmp = round(tmp, 3)
        return 340.3 * math.sqrt(tmp)


