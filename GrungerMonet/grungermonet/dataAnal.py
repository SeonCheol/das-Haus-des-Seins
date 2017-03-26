import sys
from math import *
import numpy as np
data1 = [[], [], []]
data2 = [[], [], []]
result1 = [ [], [], [] ]
result2 = [ [], [], [] ]
idx = 0

file = open("data/dataForSound.data", 'r')
while True:
    idx = idx+1
    line = file.readline()
    if not line: break
    tmpData =  line.split(" ")
    tm = float(tmpData[1])
    if tm >100:
        data1[0].append(float(tmpData[1]))
    data2[0].append(float(tmpData[5]))

    print float(tmpData[1])  ,float( tmpData[5]), idx
file.close()
result1[0].append(np.mean(data1[0]))
result1[0].append(np.var(data1[0]))
file = open("data/dataResult2.data", 'w+')
file.write(str(result1[0][0]) + " " + str(sqrt(result1[0][1])))
file.close()