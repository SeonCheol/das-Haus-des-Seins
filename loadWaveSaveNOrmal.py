from src import myWave
from src import dspUtil
import numpy as np
import copy
from src import generalUtility

fName = 'realtime_test.wav'

numChannels, numFrames, fs, data = myWave.readWaveFile(fName)

# data[0] = dspUtil.normalize(data[0])
data[0] = 0
#
# for chIdx in range(numChannels):
#     n = len(data[chIdx])
#     dataTmp = copy.deepcopy(data[chIdx])
#     for i in range(n):
#         data[chIdx][i] = dataTmp[n - (i+1)]

dataOut = [data[0], data[1]]
fileNameOnly = generalUtility.getFileNameOnly(fName)
outputFileName = fileNameOnly + "_processed.wav"
myWave.writeWaveFile(dataOut, outputFileName, fs)