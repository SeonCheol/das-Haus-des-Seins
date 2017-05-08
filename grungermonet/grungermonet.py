import numpy as np
import pyaudio
# import gcc_phat as gcc
import math
# from scipy.io import wavfile
# import matplotlib.pyplot as plt
# from pyAudioAnalysis import audioFeatureExtraction as af
import scipy.fftpack as sf
from socket import *
from select import *
import wave
import sys

from pip._vendor.ipaddress import summarize_address_range


class RingList:
    def __init__(self, length):
        self.__data__ = []
        self.__full__ = 0
        self.__max__ = length
        self.__cur__ = 0

    def append(self, x):
        if self.__full__ == 1:
            for i in range (0, self.__cur__ - 1):
                self.__data__[i] = self.__data__[i + 1]
            self.__data__[self.__cur__ - 1] = x
        else:
            self.__data__.append(x)
            self.__cur__ += 1
            if self.__cur__ == self.__max__:
                self.__full__ = 1

    def get(self):
        return self.__data__

    def remove(self):
        if (self.__cur__ > 0):
            del self.__data__[self.__cur__ - 1]
            self.__cur__ -= 1

    def size(self):
        return self.__cur__

    def maxsize(self):
        return self.__max__

    def __str__(self):
        return ''.join(self.__data__)


class GrungerMonet:
    CHUNK = 1024
    MIC_NUM = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16
    RECORD_SECONDS = 1500

    idx2 = 0

    # the time delayed from another signal
    time_delay = 0

    # signal data from mics

    ## standard to detect voice end point
    sum_energy = [0, 0]
    idx = 0
    isVoice = False

    ## to find the location
    energy_max = 1
    energy_min = -.5

    ## for solution to delay mic data
    energyList = RingList(3)

    ## for threshold reset
    threshold = RingList(200)

    diffVal = RingList(500)


    originalThresholdVal = 10000




    def __init__(se1lf):
        ## initalize the variables
        print("start the app")

    ## for the test use two record files
    def cal_location(self, delay_time):
        meter_per_dot = round(self.dist * 1.0 / self.width, 5)

        diff_from_cent = meter_per_dot * delay_time
        loc = self.width / 2 + diff_from_cent

        # print meter_per_dot, diff_from_cent, loc
        return round(loc, 5)

    def normalize(self, data, mean, std):
        normalized = data - mean
        normalized = normalized * 1.0 / std
        return normalized

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

    # def maxFrequencyForFFT(self, Spectrum, F_sample, Low_cutoff=60, High_cutoff=360):
    #     """ Searching presence of frequencies on a real signal using FFT
    #     Inputs
    #     =======
    #     X: 1-D numpy array, the real time domain audio signal (single channel time series)
    #     Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
    #     High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
    #     F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
    #     """
    #
    #     # M = X.size  # let M be the length of the time series
    #     # Spectrum = sf.rfft(X, n=M)
    #     M = Spectrum.size
    #     [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
    #
    #     # Convert cutoff frequencies into points on spectrum
    #     [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
    #     # print Low_point, High_point
    #     maximumFrequency = np.where(
    #         Spectrum == np.max(Spectrum[int(Low_point): int(High_point)]))  # Calculating which frequency has max power.
    #
    #     n = len(Spectrum)  # length of the signal
    #     k = np.arange(n)
    #     T = n / F_sample
    #     frq = k / T  # two sides frequency range
    #     frq = frq[range(int(n / 2))]  # one side frequency range
    #
    #     return frq[maximumFrequency], maximumFrequency[0]
    #
    # def decibel(self, soundVal, maxVal):
    #     dB = round(soundVal / maxVal, 4)
    #     dB = abs(dB)
    #     # print dB
    #     dB = 20 * math.log10(dB)
    #     return dB

    def deviation(self, Spectrum, F_sample, Low_cutoff=60, High_cutoff=360):
        M = Spectrum.size
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
        return math.sqrt(np.var(Spectrum[int(Low_point):int(High_point)]))


    def maxFreq(self, fftData, size):
        lowPoint = 60
        highPoint = 360
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
            frqSum += fftfrq[i + lowIdx] * int(fftData[i + lowIdx])
            sum += int(fftData[i + lowIdx])
        thefreq = frqSum * 1.0 / sum
        return maxIdx + lowIdx, thefreq

    def getFeature(self, fft_data, size):
        # maxFrq, maxFreqIdx = self.maxFrequencyForFFT(fft_data, self.RATE)
        maxFreqIdx, maxFrq = self.maxFreq(fft_data, size)
        # max_idx = np.argmax(fft_data)
        softness = self.deviation(fft_data, self.RATE)
        return np.array([maxFrq, softness])

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

    def saveEnergyToTraining(self, ene):
        file = open("data/energyDataForTrainigToLocSound.data", "a")
        file.write(str(self.sum_energy[0] * 1.0 / self.idx) + " " + str(self.sum_energy[1] * 1.0 / self.idx))
        file.write(",")

    ## ene1 : mic1 energy
    ## ene2 : mic2 energy
    def findLoc(self, ene1, ene2):

        if math.isnan(ene1) and math.isnan(ene2):
            return -100
        elif math.isnan(ene1): ene1 = 0
        elif math.isnan(ene2): ene2 = 0
            # self.energyList.append(result)
            # result = np.mean(self.energyList.__data__)
            # print "ene 1 : ", ene1, " ene2 : ", ene2, " max : ", self.energy_max, " idx: ", self.idx, self.energy_min, self.energy_max
            # return result
        diff_val = ene1 - ene2
        self.idx += 1
        self.idx %= 400
        # if(self.idx == 0):
        #     self.energy_max = 1.0
        #     self.energy_min = -.5
        # else:
        #     self.energy_max -= 0.5
        #     self.energy_min += .1

        # if diff_val > self.energy_max:
        #     self.energy_max = diff_val
        # elif diff_val < self.energy_min:
        #     self.energy_min = diff_val
        # if diff_val > 0:
        #     result = ( (diff_val - self.energy_min) * 1.0 ) / ( self.energy_max - self.energy_min)
        # else:
        #     result = diff_val * 1.0 / abs(self.energy_max)

        #result = ene1 * 1.0 / ene2
        # self.energyList.append(result)
        #print self.diffVal.__data__
        try:
            self.diffVal.append(diff_val)
            m = np.mean(self.diffVal.__data__)
            result = diff_val - m
            if result < m:
                return -.5
            else:
                return .5
            # result = result / np.std(self.diffVal.__data__)
            # result = result / 2
        except Exception as e:
            result = -100

        #result = np.mean(self.energyList.__data__)

        print "ene 1 : ", ene1, " ene2 : ", ene2, " max : ", self.energy_max, " idx: ", self.idx, " result : ", result
        return result

    def server(self):
        HOST = ''
        PORT = 5810
        BUF_SIZE = self.CHUNK
        ADDR = (HOST, PORT)
        # NUM = 2

        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(ADDR)
        serverSock.listen(10)
        connection_list = [serverSock]
        print "start. wait connecting to %s port" % str(PORT)

        ## start flag
        num_client = 0
        data = [None, None]

        while connection_list:
            try:
                # requested with select , and unblock every 10 seconds
                read_sock, write_sock, err_sock = select(connection_list, [], [], 10)
                if num_client < 2:
                    print('wait...', num_client)
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
                        # data[i] = connection_list[i + 1].recv(self.CHUNK)
                        data[i] = connection_list[i+1].recv(100)
                        if data[i]:
                            data[i] = np.fromstring(data[i])
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
                            print "exit and save"
                            num_client = 0
                            sys.exit()
                    ## after retrieve the datas
                    strToSave += " "

                    loc = self.findLoc(data[0][-1], data[1][-1])
                    if loc != -100:
                        strToSave += str(loc)
                        print strToSave

                    self.isVoice = False
                    file = open("data/dataForSound.data", "w+")
                    file.write(strToSave)
                    file.close()
            except KeyboardInterrupt:
                serverSock.close()
                sys.exit()

    def client(self):
        HOST = '127.0.0.1'
        # HOST = '39.115.18.70'
        PORT = 5810
        BUFF_SIZE = self.CHUNK
        ADDR = (HOST, PORT)

        clientSock = socket(AF_INET, SOCK_STREAM)
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=1,
                        rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        n = int((self.RATE / self.CHUNK) * self.RECORD_SECONDS)
        energyFile = open("data/energyMic1Result.data", "r")
        energyAnal = energyFile.readline().split(" ")
        energyAnal = map(float, energyAnal) ## [0]: mean ## [1]: std
        self.originalThresholdVal = energyAnal[0]
        energyFile.close()
        try:
            clientSock.connect(ADDR)
            print("wait...")
            clientSock.recv(22)
            print("Recording....")
            while True: #for i in range(0, n):
                data = stream.read(self.CHUNK)
                data = np.fromstring(data, dtype='int16')
                fft_data1 = np.fft.fft(data)
                fft_data1 = abs(fft_data1) / (len(fft_data1)/2)
                energy = np.sum(fft_data1)
                threshold = energyAnal[0] + energyAnal[1]*1.0
                # if energy > energyAnal[0] + energyAnal[1]*2.5:
                #     self.threshold.append(energy)
                m = np.mean(self.threshold.__data__)
                sq = math.sqrt(np.var(self.threshold.__data__))
                if self.threshold.size() > 100:
                    energyAnal[0] = m#np.mean(self.threshold.__data__)
                    energyAnal[1] = sq

                print "mean: ", m, " sqrt : ",  sq
                #
                # if self.originalThresholdVal < energyAnal[0]:
                #     if energy < energyAnal[0] + energyAnal[1]*2.5:
                #         self.threshold.append(energy)
                # else:
                #     if energy < energyAnal[0] + energyAnal[1]*1.5:
                #         self.threshold.append(energy)
                self.threshold.append(energy)

                if threshold < energy:  ## energy over the threshold
                    energy = self.normalize(energy, energyAnal[0], energyAnal[1])
                    feature = self.getFeature(fft_data1, data.size)
                    feature = np.append(feature, energy)
                    clientSock.send(feature.tostring())
                    clientSock.recv(22)
                else:
                    clientSock.send(np.array([-1, -1]).tostring())
                    clientSock.recv(22)
        except Exception as e:
            print(e.message)
            sys.exit()
        print("connect")