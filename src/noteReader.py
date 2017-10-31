'''
Created on Oct 26, 2017

@author: bhans
'''
def getNotes(fileName):
    
    f = open(fileName);
    
    tempo = "1p2"
    
    input = f.readline()
    
    while (input == "\n" or input[0] == "#"):
        input = f.readline()
        
    tempo = input.replace("\n", "")
    
    song = []
    
    input = f.readline()
    
    while (input != ""):
        if (input != "\n" and input[0] != "#"):
            song.append(input.replace("\n", ""))
        input = f.readline()
    
    return [tempo, song]
