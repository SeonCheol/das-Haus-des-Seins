import numpy as np
import pyaudio
import gcc_phat as gcc
import math
from scipy.io import wavfile
import matplotlib.pyplot as plt
# from pyAudioAnalysis import audioFeatureExtraction as af
# import audioSegmentation as aS
from socket import *
from select import *
import wave  ## to test
import sys

class GrungerMonet:
    CHUNK = 1024
    MIC_NUM = 2
    RATE = 44100
    FORMAT =pyaudio.paInt16
    RECORD_SECONDS = 8


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



    def play(self):
        print('playing')
        #### input voice ###
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT, channels=self.MIC_NUM,
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

        ### get delay time from gcc_PHAT ###
            delay = self.get_delay_time_gcc(data1, data2)
            print delay
        ### calculate the sound local ###
            location = self.cal_location(delay)
            print location


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
        fig = plt.figure()
        sf = fig.add_subplot(111)
        plt.xlim(0, 2048)
        mean_energy = 0

        for i in range(0, n/2):
            ### input from mic1
            data1 = stream.read(self.CHUNK*2)
            frames.append(data1)
            data1 = np.fromstring(data1, dtype='int16')
            ### input from mic2
            data2 = data1

            ### get delay time from gcc_PHAT ###
            delay = self.get_delay_time_gcc(data1, data2)

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
            location = self.cal_location(delay)
            if self.isVoice == True:
                plt.plot(location, 0.5, 'ro')
                plt.draw(), plt.pause(0.0001)
                plt.clf()
            else:
                plt.clf()

            print(energy, mean_energy, self.isVoice, self.idx)


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

        # print "max idx ", max_idx
        delay_time = max_idx - (k/2)
        delay_time = delay_time * self.dist_per_index

        return delay_time

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


    def server_play(self):

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
        while connection_list:
            try:
                print('wait...')
                # requested with select , and unblock every 10 seconds
                read_sock, write_sock, err_sock = select(connection_list, [], [], 10)
                # print read_sock, write_sock, err_sock
                print( num_client, len(connection_list), read_sock)

                if num_client < 2 :
                    for sock in read_sock:
                        if sock == serverSock:
                            clientSock, addr_info = serverSock.accept()
                            connection_list.append(clientSock)
                            num_client += 1

                            if num_client == 2:
                                for tmp_sock in connection_list[1:]:
                                    tmp_sock.send('s')
                elif num_client == 2:
                    for i in range(2):
                        data[i] = connection_list[i+1].recv(BUF_SIZE)

                        if data[i]:
                            frames[i].append(data[i])
                            data[i] = np.fromstring(data[i])
                        else:
                            print "exit and save"
                            for j in range(2):
                                # connection_list.remove(read_sock[j])
                                num_client  = 0
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
                            break
                            sys.exit()
                    ## after retrieve the datas
                    delay = self.get_delay_time_gcc(data[0], data[1])
                    # energy = af.stEnergy(data[0])
                    # if self.idx%100 == 0:
                    #     self.sum_energy = self.sum_energy + energy
                    # mean_energy = round(self.sum_energy / (self.idx + 1), 4)
                    # self.idx = self.idx + 1
                    # self.idx = self.idx % 100

                    # if mean_energy <= energy:
                    #     self.isVoice = True
                    # else:
                    #     self.isVoice = False

                    ### calculate the sound  source ###
                    location = self.cal_location(delay)
                    # if self.isVoice == True:
                    #     plt.plot(location, 0.5, 'ro')
                    #     plt.draw(), plt.pause(0.0001)
                    #     plt.clf()
                    # else:
                    #     plt.clf()
                    print(location)
            except KeyboardInterrupt:
                serverSock.close()
                sys.exit()



    def client_play(self):
        ## socket info
        HOST = '127.0.0.1'
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
        try:
            clientSock.connect(ADDR)

            print("wait...")
            clientSock.recv(22)

            print("Recording....")

            for i in range(0, n):
                data = stream.read(self.CHUNK)
                print(i)
                frames.append(data)
                clientSock.send(data)
                # data = np.fromstring(data, dtype='int16')

            wf = wave.open('test2.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

        except Exception as e:
            print(e.message)
            sys.exit()

        print("connect")
