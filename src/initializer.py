import numpy
import pyaudio
import analyse
import time

class initializer:
    
    folder = "sheet"
    song_file = "songs.txt"
    pitch_file = "pitch.txt"
    songs = {}
    pitches = {}

    def __init__(self, song_file, pitch_file, folder):
        self.song_file = song_file
        self.pitch_file = pitch_file
        self.folder = folder
        
    def getPitches(self):
        
        f = open(self.folder+'/'+self.pitch_file)
        
        input = f.readline()
        while (input != ""):
            if input != "\n":
                elements = input.replace("\n", "").replace("\r", "").split(":")
                self.pitches[elements[0]] = {"p":float(elements[1]), "v":float(elements[2])}
            input = f.readline()
        
        f.close()
        
        return self.pitches
        
    
    def getSongs(self):
        
        song_list = []
        
        f = open(self.folder+'/'+self.song_file)
        
        input = f.readline()
        while (input != ""):
            if input != "\n":
                song_list.append(input.replace("\n", "").replace("\r", ""))
            input = f.readline()
        
        f.close()
        
        for label in song_list:
        
            f = open(self.folder+'/'+label)
        
            input = f.readline()
            while input == "\n":
                input = f.readline()
            tempo = float(input.replace("\n", "").replace("\r", ""))
        
            notes = []
        
            input = f.readline()
        
            while input != "":
                if input != "\n":
                    notes.append(input.replace("\n", "").replace("\r", ""))
                input = f.readline()
                
            self.songs[label] = {'l':label, 't':float(tempo), 'n':notes}
            
            f.close()

        return self.songs