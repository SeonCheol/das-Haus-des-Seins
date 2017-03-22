import numpy as np
import pyaudio
import gcc_phat as gcc
import math
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioFeatureExtraction as af
import scipy.fftpack as sf

class GrungerMonet:
    CHUNK = 1024
    MIC_NUM = 2
    RATE = 44100
    FORMAT =pyaudio.paInt16
    RECORD_SECONDS = 20

    idx2 = 0

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
    ## this value indicate how much a index mean distance (? too short my english)
    dist_per_index = 0

    ## display
    width = 2048
    height = 1024

    ## standard to detect voice end point
    sum_energy = 0
    idx = 0
    isVoice = False

    def __init__(self, dist=3.0, temperature=15):
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
        self.dist_per_index = round( (1.0/self.RATE), 5)


        print("start the app")
    ## for the test use two record files
    def test_play(self):
        fs1, data1 = wavfile.read('sound/test_stretched_backpos.wav')
        fs2, data2 = wavfile.read('sound/test_stretched_forpos.wav')

        fs = fs1
        length = len(data1)
        n = int(length/fs)
        interval = 1

        # plt.ion()
        # fig = plt.figure()
        # sf = fig.add_subplot(111)
        dot = []
        for i in range(n):
            tmp_data1 = data1.T[0][(i * interval * fs):(i + 1) * interval * fs]
            # tmp_data2 = data2.T[0][(i*fs):(i+1)*fs]
            tmp_data2 = data2.T[0][(i * interval) * fs:(i + 1) * interval * fs]

            delay = self.get_delay_time_gcc(tmp_data1, tmp_data2)
            print delay

            location = self.cal_location(delay)
            print location
            dot.append(location)

        plt.plot(dot, range(0, len(dot)), 'ro')
        plt.show()
    ## for pyaudioanalysis test ###
    def an_test_play(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT, channels=self.MIC_NUM,
                        rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        n = int((self.RATE / self.CHUNK) * self.RECORD_SECONDS)
        frames = []

        plt.ion()

        fig, ax = plt.subplot(2, 1)
        # fig = plt.figure()
        # # sf = fig.add_subplot(111)
        # # plt.xlim(0, 2048)
        mean_energy = 0

        for i in range(0, n/2):
            ### input from mic1
            data1 = stream.read(self.CHUNK*2)
            frames.append(data1)
            data1 = np.fromstring(data1, dtype='int16')
            fft_data = np.fft.fft(data1)

            ### get delay time from gcc_PHAT ###
            # delay = self.get_delay_time_gcc(data1, data2)

            energy = af.stEnergy(data1)

            if ( (self.idx%100) == 0):
                self.sum_energy = mean_energy

            self.sum_energy = self.sum_energy + energy

            mean_energy = round(self.sum_energy / (self.idx + 1), 4)

            self.idx = self.idx + 1
            self.idx = self.idx % 100

            if mean_energy <= energy:
                self.isVoice = True
            else:
                self.isVoice = False

            # chroma = af.stChromagram(data1, self.RATE, round(self.RATE * 0.040), round(self.RATE * 0.040), True)
            # diarization = aS.speakerDiarizationCustom(data1, self.RATE, 2)

            ### calculate the sound local ###
            # location = self.cal_location(delay)
            if self.isVoice == True:
                if i%10 == 0:
                    n = len(data1)
                    t = np.arange(0, len(data1)*1.0/self.RATE, 1.0/self.RATE)
                    k = np.arange(n)
                    T = n/self.RATE
                    frq = k/T
                    frq = frq[range(int(n/2))]

                    ax[0].plot(t, data1)
                    ax[0].set_xlabel('Time')
                    ax[0].set_ylabel('Amplitude')
                    ax[1].plot(frq, abs(fft_data), 'r')  # plotting the spectrum
                    ax[1].set_xlabel('Freq (Hz)')
                    ax[1].set_ylabel('|Y(freq)|')
                    plt.draw(), plt.pause(0.0001)
                    plt.clf()
            else:
                plt.clf()

            print(energy, mean_energy, self.isVoice, self.idx)
    def cal_location(self, delay_time):
        meter_per_dot = round(self.dist*1.0 / self.width, 5)

        diff_from_cent = meter_per_dot * delay_time
        loc = self.width/2 + diff_from_cent

        # print meter_per_dot, diff_from_cent, loc
        return round(loc, 5)
    ## get sound speed
    def sound_speed(self, temperature=15):
        tmp = (273 + temperature) / 288
        tmp = round(tmp, 3)
        return 340.3 * math.sqrt(tmp)
    ## return fft_result and frq axis array
    def maxFrequency(X, F_sample, Low_cutoff=80, High_cutoff=300):
        """ Searching presence of frequencies on a real signal using FFT
        Inputs
        =======
        X: 1-D numpy array, the real time domain audio signal (single channel time series)
        Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
        High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
        F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
        """

        M = X.size  # let M be the length of the time series
        Spectrum = sf.fft(X, n=M)
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])

        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])

        maximumFrequency = np.where(
            Spectrum == np.max(Spectrum[Low_point: High_point]))  # Calculating which frequency has max power.

        return maximumFrequency
    def maxFrequencyForFFT(self, Spectrum, F_sample, Low_cutoff=80, High_cutoff=300):
        """ Searching presence of frequencies on a real signal using FFT
        Inputs
        =======
        X: 1-D numpy array, the real time domain audio signal (single channel time series)
        Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
        High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
        F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
        """

        # M = X.size  # let M be the length of the time series
        # Spectrum = sf.rfft(X, n=M)
        M = Spectrum.size
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])

        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
        # print Low_point, High_point
        maximumFrequency = np.where(
            Spectrum == np.max(Spectrum[int(Low_point): int(High_point)]))  # Calculating which frequency has max power.

        n = len(Spectrum)  # length of the signal
        k = np.arange(n)
        T = n / F_sample
        frq = k / T  # two sides frequency range
        frq = frq[range(int(n / 2))]  # one side frequency range

        return frq[maximumFrequency], maximumFrequency[0]
    def decibel(self, soundVal, maxVal):
        dB = round(soundVal/ maxVal, 4)
        dB = abs(dB)
        # print dB
        dB = 20* math.log10(dB)
        return dB
    def deviation(self, Spectrum, F_sample, Low_cutoff=80, High_cutoff=300):
        M = Spectrum.size
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
        return np.var(Spectrum[int(Low_point):int(High_point)])
    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.MIC_NUM,
                        rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        n = int((self.RATE / self.CHUNK) * self.RECORD_SECONDS)
        frames = []
        mean_energy = 0
        for i in range(0, n):
            data = stream.read(self.CHUNK)
            frames.append(data)
            data = np.fromstring(data, dtype='int16')
            data2 = data

            energy = af.stEnergy(data)
            print("energy " ,energy)
            if ( (self.idx%100) == 0):
                self.sum_energy = mean_energy
            self.sum_energy = self.sum_energy + energy
            mean_energy = round(self.sum_energy / (self.idx + 1), 4)
            self.idx = self.idx + 1
            self.idx = self.idx % 100
            if mean_energy <= energy:
                self.isVoice = True
            else:
                self.isVoice = False
            fft_data1 = np.fft.fft(data)
            fft_data2 = np.fft.fft(data2)
            feature = self.getFeature(fft_data1)
            self.saveFile(feature)
            print feature, self.idx2

    def getFeature(self, fft_data):
        maxFrq, maxFreqIdx = self.maxFrequencyForFFT(fft_data, self.RATE)
        max_idx = np.argmax(fft_data)
        decibel = self.decibel(fft_data[maxFreqIdx][0], max_idx)
        softness = self.deviation(fft_data, self.RATE)
        return maxFrq[0], decibel, softness

    def saveFile(self, toSaveData):
        #fileName = "dataForsoundInfo" + str(self.idx2) + ".txt"
        fileName="data/dataForsoundInfo0.txt";
        file = open(fileName, 'w+')
        for i in range(3):
            file.write(str(toSaveData[i]) + " ")
        file.write(str(self.idx2))
        self.idx2 += 1
        self.idx2 = int(self.idx2 % 1000000)
        file.close()