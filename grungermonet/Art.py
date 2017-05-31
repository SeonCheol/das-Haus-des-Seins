import Sound
import numpy as np
import math
from socket import *
from select import *
import sys
from RingList import *

def normalize(data, mean, std):
    return (data - mean) * 1.0 / std

class GrungerMonet:
    def __init__(self):
        self.energyList = RingList(3)
        self.threshold = RingList(200)
        self.diffVal = RingList(500)
        self.originalThresholdVal = 10000

    def findLoc(self, ene1, ene2):
        if math.isnan(ene1) and math.isnan(ene2):
            return -100
        elif math.isnan(ene1):
            ene1 = 0
        elif math.isnan(ene2):
            ene2 = 0

        diff_val = ene1 - ene2
        try:
            self.diffVal.append(diff_val)
            m = np.mean(self.diffVal.__data__)
            result = diff_val - m
            if result < m:
                return -.5
            else:
                return .5
        except Exception as e:
            result = -100

        return result

    def server(self):
        HOST = ''
        PORT = 5810
        BUF_SIZE = Sound.CHUNK
        ADDR = (HOST, PORT)

        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(ADDR)
        serverSock.listen(10)
        connection_list = [serverSock]
        print "start~ wait connecting to %s port" % str(PORT)

        ## start flag
        num_client = 0
        data = [None, None]

        while connection_list:
            try:
                read_sock, write_sock, err_sock = select(connection_list, [], [], 10)
                if num_client < 2:
                    print('wait... ', num_client)
                    for sock in read_sock:
                        if sock == serverSock:
                            clientSock, addr_info = serverSock.accept()
                            connection_list.append(clientSock)
                            num_client += 1
                            if num_client == 2:
                                for tmp_sock in connection_list[1:]:
                                    tmp_sock.send('s')
                elif num_client == 2:
                    strToSave = ''
                    for i in range(2):
                        data[i] = connection_list[i+1].recv(100)
                        if data[i]:
                            data[i] = np.fromstring(data[i])
                            try:
                                if math.isnan(data[i][0]):
                                    strToSave += str(-1) + " "
                                else:
                                    strToSave += str(i) + " "
                                    for j in range(len(data[i])):
                                        strToSave += str(data[i][j]) + " "
                                connection_list[i+1].send('s')
                            except ValueError as e:
                                print e.message
                        else:
                            print 'exit'
                            num_client = 0
                            sys.exit()
                    ## after retrieve the datas
                    strToSave += " "

                    loc = self.findLoc(data[0][-1], data[1][-1])
                    if loc != -100:
                        strToSave += str(loc)
                        print strToSave
                    file = open("data/dataForSound.data", "w+")
                    file.write(strToSave)
                    file.close()
            except KeyboardInterrupt:
                serverSock.close()
                sys.exit()

    def client(self):
        HOST = '127.0.0.1'
        PORT = 5810
        BUF_SIZE = Sound.CHUNK
        ADDR = (HOST, PORT)
        clientSock = socket(AF_INET, SOCK_STREAM)
        self.sound = Sound.MyAudio()

        energyFile = open("data/energyMicResult.data", "r")
        energyAnal = energyFile.readline().split(" ")
        energyAnal = map(float, energyAnal) ## [0]: mean ## [1]: std
        self.originalThresholdVal = energyAnal[0]
        energyFile.close()
        ##try:
        clientSock.connect(ADDR)
        print('wait...')
        clientSock.recv(22)
        print("Recording...")
        while True:
            self.sound.update()
            fft = self.sound.fft_data
            energy = np.sum(fft)
            if not (None == energy):
                self.threshold.append(energy)

            threshold = energyAnal[0] + energyAnal[1] * 1.0

            m = np.mean(self.threshold.__data__)
            sq = np.std(self.threshold.__data__)
            if self.threshold.size() > 100:
                energyAnal[0] = m
                energyAnal[1] = sq

            if threshold < energy:
                energy = round(normalize(energy, energyAnal[0], energyAnal[1]), 4)
                print energy
                feature = self.sound.getFeature()
                print " pre ", feature
                feature = np.append(feature, energy)

                print "feature : " , feature
                clientSock.send(np.array(feature).tostring())
                clientSock.recv(22)
            else:
                clientSock.send(np.array([-1, -1]).tostring())
                clientSock.recv(22)
        ##except Exception as e:
            # print e.message
            # sys.exit()
        print "connect"