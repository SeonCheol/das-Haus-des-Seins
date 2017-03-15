from src import praatTextGrid, myWave, generalUtility
import os

path = 'C:/Users/seoncheol/Documents/python/python_for_sound/'

suffix = 'wav'

for fName in os.listdir(path):
    if fName.split('.')[-1] == suffix:
        print(fName)

        fileNameOnly = generalUtility.getFileNameOnly(fName)
        outputFileName = path + fileNameOnly + '.TextGrid'
        if os.path.isfile(outputFileName):
            print("\tWARNING: TextGrid already exists")
        else:
            numChannels, numFrames, fs, data = myWave.readWaveFile(path+fName)
            n = len(data[0])
            duration = float(n) / float(fs)

            textGrid = praatTextGrid.PraatTextGrid(0, duration)

            intervalTier = praatTextGrid.PraatIntervalTier('myAnnotaion')

            intervalTier.add(0, duration, '')
            print(intervalTier)
            textGrid.add(intervalTier)
            textGrid.save(outputFileName)
