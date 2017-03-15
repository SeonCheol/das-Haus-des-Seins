
import pyaudio
import wave
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60

WAVE_OUTPUT_FILENAME = "test.wav"



#wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate = RATE,
                input = True,
                output= True,
                frames_per_buffer=CHUNK)

print("*** Recording audio....")
# record voice
frames = []

#read data
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    stream.write(data)

# play stream (3)
#while len(data) > 0:
  #  stream.write(data)
    #data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
