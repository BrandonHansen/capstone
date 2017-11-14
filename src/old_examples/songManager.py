'''
Created on Oct 26, 2017

@author: bhans
'''

class songManager:
    
    tempo = 1
    song = []
    
    def __init__(self, tempo, song):
        self.tempo = tempo
        self.song = song
        
    def readTextForComposition(self, fileName):
        f = open(fileName)
        
        input = f.readline()
        
        while (input == "\n" or input[0] == "#"):
            input = f.readline()
            
        tempo = input.replace("\n", "")
        
        input = f.readline()
        
        while (input != ""):
            if (input != "\n" and input[0] != "#"):
                self.song.append(input.replace("\n", ""))
            input = f.readline()
        
    def getSong(self):
        return self.song
    
    def getNote(self, index):
        return self.song[index]
    
    def getTempo(self):
        return  self.tempo