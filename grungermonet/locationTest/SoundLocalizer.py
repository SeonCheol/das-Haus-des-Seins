from math import *
import time, threading
import Queue
from abc import ABCMeta, abstractmethod


class OnMatchListener(object):
    def __init__(self):
        self.position = -100

    def notify(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def reset(self):
        self.position = -100


"""
Localizer is the class for sound localization
This class is made by observer pattern with OnMatchListener class
"""


class Localizer(threading.Thread):
    soundSpeed = 340.29
    queue1 = Queue.Queue()
    queue2 = Queue.Queue()
    ## mic distance

    def __init__(self, listener, dist=2.0):
        threading.Thread.__init__(self)
        self.observer = listener
        self.dist = dist
        self.maxDiffVal = self.dist / self.soundSpeed
        self.minDiffVal = 1.0
        print "max: " , self.maxDiffVal


    def isMatchable(self):
        return (not self.queue1.empty()) and (not self.queue2.empty())

    def run(self):
        while True:
            if self.isMatchable():
                ## matching
                #with self.queue1.mutex:
                item1 = self.queue1.get(False)
                #with self.queue2.mutex:
                item2 = self.queue2.get(False)
                position = self.findLocation(item1, item2)
                ##calculate position
                print("position is ", position)
                self.observer.notify(position)
            else:
                if self.queue1.qsize() > 2:
                    self.queue1.get(False)
                if self.queue2.qsize() > 2:
                    self.queue2.get(False)

    ### return value -100 mean  the difference value between time1,2
    ### meaningless value
    def findLocation(self, time1, time2):
        diff = time1 - time2

        if abs(diff) > 1:
            return -100
        # if diff > self.maxDiffVal:
        #     diff = self.maxDiffVal
        # elif diff < self.maxDiffVal * -1:
        #     diff = self.maxDiffVal * -1

        if diff > self.maxDiffVal:
            self.maxDiffVal = diff
        elif diff < self.minDiffVal:
            self.minDiffVal = diff
        print "diff : ", diff, "max : ", self.maxDiffVal, " min : ", self.minDiffVal
        try:
            return (diff - self.minDiffVal) / ( self.maxDiffVal - self.minDiffVal )
        except ZeroDivisionError as e:
            return 0.5

    def updateQueue(self, time1, time2):
        if time1 != -1 and not isnan(time1):
            print "time1 : ", time1
            self.queue1.put(time1)
        if time2 != -1 and not isnan(time2):
            print "time2 : ", time2
            self.queue2.put(time2)








#####################################
########
#### in main thread
#
#
#
# Localizer(new OnMatchListener() {
#         @Override
#         void onMatch(float position) {
#             ## using position, update processing's display
#         }
#  ));