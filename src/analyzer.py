import numpy
import pyaudio
import analyse
import time

class analyzer:
    
    expected = []
    actual = []
    pitches = {}
    
    def __init__(self, song, pitches):
        self.expected = song
        self.pitches = pitches
    
    def resetAnalyzer(self):
        actual = []
    
    def analyzeSegment(self, segment):
        presence_score = 1
        loudness_score = 1
        pitch_count = {}
        
        #for pitch in pitches:
        #    pitch_count[pitch] = 0
        
        for entry in segment:
            pitch = self.judgeSound(entry['p'])
            if pitch != None:
                if pitch != pitch_count:
                    pitch_count[pitch] = 0
                pitch_count[pitch] += entry['v']
        
        if len(pitch_count) > 0:
            max_value = max(pitch_count, key=lambda i: pitch_count[i])
        else:
            return [None, 0]
        
        if pitch_count[max_value] == 0:
            return [None, 0]
                
        return [max_value, pitch_count[max_value]]
        
        
    def judgeSound(self, sound):
        if sound == None:
            return None
        for pitch in self.pitches:
            upper = self.pitches[pitch]['p'] + self.pitches[pitch]['v']
            lower = self.pitches[pitch]['p'] - self.pitches[pitch]['v']
            if (sound >= lower) and (sound <= upper):
                return pitch
        return None
    
    def addAnalysis(self, note):
        self.actual.append(note)
        
    def scoreSong(self):
        
        score = 0.0
        
        elength = len(self.expected)
        alength = len(self.actual)
        
        total = min(elength, alength)
        
        count = 0
        while count < total:
            if str(self.expected[count]) == str(self.actual[count]):
                score += 1.0
            count += 1
        
        final_score = int((score/total)*100)
        
        return final_score


