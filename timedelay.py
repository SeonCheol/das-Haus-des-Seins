#import correlate
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import time
import gcc_phat as gcc

# only signal data in data variable
def get_delay(data1, data2, fs):
    if  len(data1) != len(data2):
        print("length is different")
        exit(-1)

    length = len(data1)
    #t = np.arange(0, length/fs, 1.0/fs)

    fft_data1 = np.fft.fft(data1)
    fft_data2 = np.fft.fft(data2)

    correlation = np.correlate(fft_data1, fft_data2, 'full')
    max_idx = np.argmax(correlation)
    #correlation = correlation / correlation[max_idx]

    sec = length/2
    sec = abs(sec - max_idx) / fs

    return (sec, correlation)


if '__main__' == __name__:

    fs1, data1 = wavfile.read('sound/realtime_test1.wav')
    fs2, data2 = wavfile.read('sound/realtime_test2.wav')

    # if fs1 != fs2:
    #     print("sampling is not equal")
    #     exit(-1)
    #
    # if len(data1) != len(data2):
    #     print('length is different')
    #     exit(-1)
    fs = fs1
    length = len(data1)
    interval = 1

    n = int(length/fs/interval)

    # fig, ax = plt.subplots(111)
    print(data1)

    plt.ion()
    fig = plt.figure()
    sf = fig.add_subplot(111)

    for i in range(n):  # slice the length from sampling rate
        tmp_data1 = data1.T[0][(i*interval*fs):(i+1)*interval*fs]
        # tmp_data2 = data2.T[0][(i*fs):(i+1)*fs]
        tmp_data2 = data2.T[0][(i*interval)*fs:(i+1)*interval*fs]

        gcc_result = gcc.xcorr_freq(tmp_data1, tmp_data2)

        fft_data1 = np.fft.fft(tmp_data1)
        fft_data2 = np.fft.fft(tmp_data2)
        correlation = np.correlate(fft_data1, fft_data2, 'full')


        max_idx = np.argmax(correlation)
        # correlation = correlation / correlation[max_idx]
        gcc_max_idx = np.argmax(gcc_result)

        sec = len(correlation) / 2
        sec = abs(sec - max_idx) / (fs)

        #delay_time = get_delay(tmp_data1, tmp_data2, fs)

        k = len(correlation)
        t = np.arange(-k/fs/2, k/fs/2, 1.0/fs)

        gcc_sec = len(gcc_result) / 2
        gcc_sec = abs(gcc_sec - gcc_max_idx) / (fs)
        print(t[max_idx], t[gcc_max_idx], gcc_sec)

        # plt.plot(np.arange(0, len(fft_data2)), fft_data2)
        # plt.plot(t, correlation, 'r')
        plt.plot(t, gcc_result)
        plt.draw(), plt.pause(0.0001)
        time.sleep(1.2)
        plt.clf()