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


class Localizer(threading.Thread):
    soundSpeed = 340.29
    queue1 = Queue.Queue()
    queue2 = Queue.Queue()
    ## mic distance
    dist = 2.0

    def __init__(self, listener):
        threading.Thread.__init__(self)
        self.observer = listener
        self.maxDiffVal = self.dist / self.soundSpeed

    def isMatchable(self):
        return (not self.queue1.empty()) and (not self.queue2.empty())

    def run(self):
        while True:
            if self.isMatchable():
                ## matching
                with self.queue1.mutex:
                    item1 = self.queue1.get()
                with self.queue2.mutex:
                    item2 = self.queue2.get()
                self.findLocation(item1, item2)
                ##calculate position
                position = 0.3
                self.observer.notify(position)
            else:
                with self.queue1.mutex:
                    self.queue1.queue.clear()
                with self.queue2.mutex:
                    self.queue2.queue.clear()

    def findLocation(self, time1, time2):
        diff = time1 - time2
        if diff > self.maxDiffVAl:
            diff = self.maxDiffVal
        elif diff < self.maxDiffVal * -1:
            diff = self.maxDiffVal * -1
        return diff / self.maxDiffVal

    def updateQueue(self, time1, time2):
        if time1 != -1:
            self.queue1.put(time1)
        if time2 != -1:
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