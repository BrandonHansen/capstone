import numpy
import pyaudio
import analyse
import time

class sampler:

    pointer = 0
    range = [[]]

    def __init__(self):
        pass
        #self.pointer = -1
        #self.range = []

    def advanceSegment(self):
        self.range.append([])
        self.__addPointer()

    def getSegment(self, index):
        try:
            return self.range[index]
        except Exception as e:
            print "--> exception in sampler.getSegment, probably index out of bounds"
            print e

    def getSegmentEntries(self, index, entry):
        segment = []
        
        try:
            segment = self.range[index]
        except Exception as e:
            print "--> exception in sampler.getSegment, probably index out of bounds"
            print e
        
        entries = []

        for entry in segment:
            entries.append(entry[entry])

        return entries

    def appendSegment(self, pitch, volume):
        self.range[self.pointer].append({'p':pitch, 'v':volume})

    def getLength(self):
        return len(self.range)

    def getPointer(self):
        return self.pointer
    
    def __addPointer(self):
        if self.pointer < len(self.range):
            self.pointer += 1
        else:
            print "--> pointer upper bound set, pointer equals ", self.pointer


    def __subPointer(self):
        if self.pointer > 0:
            self.pointer -= 1
        else:
            print "--> pointer lower bound set, pointer equals ", self.pointer


