import wave
from socket import *
from select import select
import sys
import numpy as np
import pyaudio
from scipy.fftpack import fft

## socket info
HOST = '127.0.0.1'
PORT = 5810
BUFF_SIZE = 1024
ADDR = (HOST, PORT)

## record info
CHUNK = 1024
MIC_NUM = 1
RATE = 44100
FORMAT =pyaudio.paInt16
RECORD_SECONDS = 1000

clientSock = socket(AF_INET, SOCK_STREAM)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=1,
                rate=RATE, input=True, frames_per_buffer=CHUNK)
n = int( (RATE / CHUNK) * RECORD_SECONDS)
frames = []
try:
    clientSock.connect(ADDR)

    print("wait...")
    clientSock.recv(22)

    print("Recording....")

    for i in range(0, n):
        data = stream.read(CHUNK)
        print(i)
        frames.append(data)
        clientSock.send(data)
        data = np.fromstring(data, dtype='int16')



    wf = wave.open('ki2.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

except Exception as e:
    print(e.message)
    sys.exit()

print("connect")