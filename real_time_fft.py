import pyaudio
import wave
import numpy as np
import timedelay as td
import gcc_phat as gcc
import matplotlib.pyplot as plt
import matplotlib.animation as anim

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "sound/test.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
n = int( (RATE / CHUNK) * RECORD_SECONDS)

## realtime graph
plt.ion()
fig = plt.figure()
sf = fig.add_subplot(111)


for i in range(0, n):
    data = stream.read(CHUNK)
    frames.append(data)
    data = np.fromstring(data, dtype='int16')
    # delay_time, cor = td.get_delay(data, data, RATE)
    fft_data = np.fft.fft(data)
    fft_data = abs(fft_data[range(int(len(fft_data)/2))])
    frq = np.fft.fftfreq(data.size, d=1.0/RATE)
    frq = frq[range(int(len(frq)/2))]
    #gcc_result = gcc.xcorr_freq(data, data)
    # k = int(len(gcc_result)/2)
    # t = np.arange(-k / RATE, k / RATE, 1.0 / RATE)
    # max_idx = np.argmax(gcc_result)
    # delay_time = abs((max_idx+1) - k/2) /RATE

    #plt.plot(t, gcc_result[1:])
    # plt.plot(data)
    plt.plot(frq, fft_data)
    plt.draw(), plt.pause(0.00001)
    plt.clf()

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
print(wf)

wf.close()