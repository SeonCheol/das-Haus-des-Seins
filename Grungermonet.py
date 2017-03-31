import numpy as np
import pyaudio
import gcc_phat as gcc
import math
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioFeatureExtraction as af
import scipy.fftpack as sf
from socket import *
from select import *
import wave
import sys

class GrungerMonet:
    CHUNK = 2048
    MIC_NUM = 2
    RATE = 44100
    FORMAT =pyaudio.paInt16
    RECORD_SECONDS = 400

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
    sum_energy = [0, 0]
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
    def maxFreq(self, fftData,  size):
        lowPoint = 95
        highPoint = 300
        sum = 0
        frqSum = 0

        fftfrq = np.fft.fftfreq(size, d=1.0 / self.RATE)
        fftfrq = fftfrq[range(int(size / 2))]

        lowIdx = np.searchsorted(fftfrq, lowPoint)
        highIdx = np.searchsorted(fftfrq, highPoint)
        tmp = fftData[lowIdx:highIdx]

        maxIdx = tmp.argmax()
        # print maxIdx,  " Max", tmp
        for i in range(maxIdx - 1, maxIdx + 1):
            frqSum += fftfrq[i + lowIdx] * int(fftData[i+lowIdx])
            sum += int(fftData[i+lowIdx])
        thefreq = frqSum * 1.0 / sum
        return maxIdx + lowIdx, thefreq
    def getFeature(self, fft_data, size):
        # maxFrq, maxFreqIdx = self.maxFrequencyForFFT(fft_data, self.RATE)

        maxFreqIdx, maxFrq  = self.maxFreq(fft_data, size)
        max_idx = np.argmax(fft_data)
        decibel = self.decibel(fft_data[maxFreqIdx], fft_data[max_idx])
        softness = self.deviation(fft_data, self.RATE)
        return np.array([maxFrq, decibel, softness])
    #
    # def saveFile(self, toSaveData):
    #     #fileName = "dataForsoundInfo" + str(self.idx2) + ".txt"
    #     fileName="data/dataForsoundInfo.data";
    #     file = open(fileName, 'a')
    #     for i in range(3):
    #         file.write(str(toSaveData[i]) + ",")
    #     file.write(str(self.idx2))
    #     self.idx2 += 1
    #     self.idx2 = int(self.idx2 % 1000000)
    #     file.write("\n")
    #     file.close()


    def findLoc(self, ene1, ene2):
        idx += 1
        if idx == 1:
            self.sum_energy[0] = 0
            self.sum_energy[1] = 0

            ## save the data for training
            file = open("data/energyDataForTrainigToLocSound.data", "a")
            file.write(str(self.sum_energy[0]) + " " + str(self.sum_energy[1]))
            file.write(",")


        self.sum_energy[0] += ene1
        self.sum_energy[1] += ene2

        mean1 = self.sum_energy[0] * 1.0 / idx
        mean2 = self.sum_energy[1] * 1.0 / idx

        idx = idx % 10


    def server(self):
        HOST = ''
        PORT = 5810
        BUF_SIZE = 1024
        ADDR = (HOST, PORT)
        NUM = 2

        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(ADDR)
        serverSock.listen(10)
        connection_list = [serverSock]
        print "start. wait connecting to %s port" % str(PORT)
        frames = [[], []]
        p = pyaudio.PyAudio()
        ## start flag
        start = False
        num_client = 0
        data = [None, None]
        idx = 0
        sum = 0

        while connection_list:
            try:
                print('wait...', num_client)
                # requested with select , and unblock every 10 seconds
                read_sock, write_sock, err_sock = select(connection_list, [], [], 10)
                if num_client < 2:
                    for sock in read_sock:
                        if sock == serverSock:
                            clientSock, addr_info = serverSock.accept()
                            connection_list.append(clientSock)
                            num_client += 1

                            if num_client == 2:
                                for tmp_sock in connection_list[1:]:
                                    tmp_sock.send('s')
                elif num_client == 2:
                    strToSave = ""
                    for i in range(2):
                        data[i] = connection_list[i + 1].recv(1024)
                        frames[i].append(data[i])
                        if data[i]:
                            data[i] = np.fromstring(data[i])
                            print data[i] , i
                            try:
                                if math.isnan(data[i][0]):
                                    strToSave += str(-1) + " "
                                else:
                                    strToSave  += str(i) + " "
                                    for j in range(len(data[i])):
                                        strToSave += str(data[i][j]) + " "
                                    # print strToSave
                                connection_list[i + 1].send('s')
                            except ValueError as e:
                                print(e.message)
                        else:
                            # print "exit and save"
                            for j in range(2):
                                # connection_list.remove(read_sock[j])
                                num_client = 0
                                filename = 'test' + str(j) + '.wav'
                                wf = wave.open(filename, 'wb')
                                wf.setnchannels(1)
                                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                                wf.setframerate(self.RATE)
                                wf.writeframes(b''.join(frames[j]))
                                wf.close()
                                connection_list[1].close()
                                connection_list.remove(connection_list[1])
                                print("the connection is closed", connection_list, j)
                            sys.exit()
                    ## after retrieve the datas
                    strToSave += "\n"
                    file = open("data/dataForSound.data", "w+")
                    file.write(strToSave)
                    file.close()
            except KeyboardInterrupt:
                serverSock.close()
                sys.exit()
    def client(self):
        ## socket info
        HOST = '127.0.0.1'
        # HOST = '39.115.18.70'
        PORT = 5810
        BUFF_SIZE = 1024
        ADDR = (HOST, PORT)

        ## record info
        # CHUNK = 1024
        # MIC_NUM = 1
        # RATE = 44100
        # FORMAT = pyaudio.paInt16
        # RECORD_SECONDS = 1000

        clientSock = socket(AF_INET, SOCK_STREAM)
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=1,
                        rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        n = int((self.RATE / self.CHUNK) * self.RECORD_SECONDS)
        frames = []
        energyFile = open("data/voiceEnergyResult.data", "r")
        energyAnal = energyFile.readline().split(" ")
        energyFile.close()
        try:
            clientSock.connect(ADDR)
            print("wait...")
            clientSock.recv(22)
            print("Recording....")
            mean_energy = 0
            for i in range(0, n):
                data = stream.read(self.CHUNK)
                frames.append(data)
                # clientSock.send(data)
                data = np.fromstring(data, dtype='int16')
                energy = af.stEnergy(data)
                if float(energyAnal[0])* 9.0/10< energy:
                    fft_data1 = np.fft.fft(data)
                    fft_data1 = abs(fft_data1)
                    feature = self.getFeature(fft_data1, data.size)
                    clientSock.send(feature.tostring())
                    clientSock.recv(22)
                else:
                    clientSock.send(np.array([-1, -1]).tostring())

                    clientSock.recv(22)

            # wf = wave.open('test.wav', 'wb')
            # wf.setnchannels(1)
            # wf.setsampwidth(p.get_sample_size(self.FORMAT))
            # wf.setframerate(self.RATE)
            # wf.writeframes(b''.join(frames))
            # wf.close()
        except Exception as e:
            print(e.message)
            sys.exit()
        print("connect")