'''
Created on Oct 26, 2017

@author: bhans
'''
import numpy
import pyaudio
import analyse
import time
from numpy import average

class pitchGetter(object):
    
    set = {}
    
    def __init__(self, set):
        self.set = set
        
    def loadPitch(self, fileName):
        
        f = open(fileName)
        
        input = f.readline()
        
        while (input != ""):
            if (input != "\n" and input[0] != "#"):
                parse1 = input.replace(" ", "").replace("\n", "").split(":")
                parse2 = parse1[1].split(",")
                self.set[parse1[0]] = [float(parse2[0]), float(parse2[1])]
            input = f.readline()
        
    def recordPitch(self, notes):
        
        seconds = 2
        
        pyaud = pyaudio.PyAudio()
        
        stream = pyaud.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            input_device_index = 2,
            input = True)
        
        f = open("sheet/test3", "w")
        
        for note in notes:
            print "start "+note
            raw_input("press any key to go")
            f.write(note+"\n")
            current = time.clock()
            running = []
            while time.clock() - current  < seconds:
                rawsamps = stream.read(1024)
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
                note_in = analyse.musical_detect_pitch(samps)
                f.write(str(note_in)+"\n")
                #print "running", time.clock(), note_in
                if note_in != None:
                    running.append(note_in)
            avg = numpy.average(running)
            std = numpy.std(running)
            self.set[note] = [avg, std]
        print "finished"
        
    def pitchTester(self):
        
        pyaud = pyaudio.PyAudio()
        
        stream = pyaud.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            input_device_index = 2,
            input = True)
        
        while True:
            rawsamps = stream.read(1024)
            samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            note_in = analyse.musical_detect_pitch(samps)
            if note_in != None:
                print note_in
'''        
getter = pitchGetter({})
getter.pitchTester()
'''