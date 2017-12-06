import numpy
import pyaudio
import analyse
import time
import sampler
import initializer
import analyzer
import thread
import sys
import math
import os
import requests

class organizer:

    inl = initializer.initializer("songs.txt", "pitch.txt", "/home/pi/capstone/src/sheet")
    songs = {}
    pitch = {}
    var = ''
    #sample analyzer or samplyzer
    wfile = open("output.txt", 'a')
    #wfile.write('instance,'+str(time.time())+',X\n')

    def __init__(self):
        #song = {'l':"test", 't':0.1, 'n':['A','B','C','D','E']}
        self.songs = self.inl.getSongs()
        self.pitch = self.inl.getPitches()

    def writeOut(self, type, data):
        r = requests.post('http://http://handbellhelper.cse.nd.edu/', data = {'key' : data})
        self.wfile.write(type+','+data+'\n')

    def printOptions(self):
        
        print "help > display this help list"
        print "song > display songs in library"
        print "play > play a song in library"
        print "exit > close this program"

    def printLibrary(self):
        
        list = "songs"
        
        for song in self.songs:
            print "Name> "+song
            list = list+','+song
            
        #self.writeOut("songs", list)

    def shell_interface(self):


        display = ">>Welcome to Hand Bell Helper, choose an option 'help'>> "

        inp = "continue"

        while inp != 'exit':
            
            inp = raw_input(display)
            elements = inp.split(' ')
            if inp == 'help':
                self.printOptions()
            elif inp == 'song' or inp == 'songs':
                self.printLibrary()
            elif elements[0] == 'play':
                if len(elements) < 2:
                    title = raw_input("Which song> ")
                else:
                    title = elements[1]
                if self.songs.get(title) != None:
                    self.startPlaying(self.songs[title])
                else:
                    print "<song does not exist>"
            elif inp == 'exit' or inp == 'quit':
                inp = 'exit'
            else:
                print "<not an option (:-/ >"

            display = ">> "

    def cmd_interface(self, input1, input2, input_var):
        
        self.var = input_var
        
        if input1 == '-song':
            self.printLibrary()
        elif input1 == '-reset':
            self.wfile.close()
            self.wfile = open("write.csv", 'w')
            self.wfile.write("")
        elif input1 == '-play':
            if input2 != None:
                if self.songs.get(input2) != None:
                    self.startPlaying(self.songs[input2])                    
                    self.wfile.close()
                    print 'done'
                else:
                    message = "<song dos not exist>"
                    print message
                    #self.writeOut("message", message)
            else:
                message =  "<no song given>"
                print message
                #self.writeOut("message", message)
        else:
            message = "<invalid command>"
            print message
            #self.writeOut("message", message)
            


    def startPlaying(self, song):
        
        
        sml = sampler.sampler()
        
        notes = song['n']
        tempo = song['t']
        
        anl = analyzer.analyzer(notes, self.pitch)
        
        pyaud = pyaudio.PyAudio()
        
        trip = False

        for i in range(pyaud.get_device_count()):
            dev = pyaud.get_device_info_by_index(i)
            if dev['name'] == 'USB PnP Sound Device: Audio (hw:1,0)':
                index = i
                trip = True
                break

        if trip == False:
            message = "--> microphone not detected"
            print message
            #self.writeOut("error", message)
            pyaud.terminate()
            return
        
        stream = pyaud.open(
                format = pyaudio.paInt16,
                channels = 1,
                rate = 44100,
                input_device_index = i,
                input = True,
                frames_per_buffer = 1024)

        listy = []
        thread.start_new_thread(self.interrupter, (listy,))


        count = 5
        message = "<starting in>"
        print '\n'+message
        #self.writeOut("message", message)
        current = time.clock()
        tracker = time.clock()
        message = str(count)
        sys.stdout.write(message+" ")
        sys.stdout.flush()
        #self.writeOut("count", message)
        while ((time.clock() - current) < 5) and (not listy):
            #print (time.clock() - tracker)
            if (time.clock() - tracker) > 1:    
                tracker = time.clock()
                count -= 1
                message = str(count)
                sys.stdout.write(message+" ")
                sys.stdout.flush()
                #self.writeOut("count", message)
        print ''

        if listy:
            message = "<song interrupted>"
            print message
            #self.writeOut("message", message)
            stream.stop_stream()
            stream.close()
            pyaud.terminate()
            return
    

        counter = 1

        for note in notes:
            print "<play note "+str(note)+" >"
            #self.writeOut("note_play", str(note))
            current = time.clock()
            tracker = time.clock()
            count = int(tempo)
            sys.stdout.write(str(count)+" ")
            sys.stdout.flush()
            while ((time.clock() - current)*10 < tempo) and (not listy) and (os.getenv(self.var, 'CONT') != 'STOP'):
                
                if (time.clock() - tracker)*10 > 1:    
                    tracker = time.clock()
                    count -= 1
                    message = str(count)
                    sys.stdout.write(message+" ")
                    sys.stdout.flush()
                    #self.writeOut("count", message)           

                # Read raw microphone data
                rawsamps = stream.read(1024, exception_on_overflow = False)
                # Convert raw data to NumPy array
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
                # Show the volume and pitch
                volume = analyse.loudness(samps)
                pitch = analyse.musical_detect_pitch(samps)
                #print (volume)*-1, pitch
                sml.appendSegment(pitch, (volume)*-1)
                
            sys.stdout.flush()
            dub  = anl.analyzeSegment(sml.getCurrentSegment())
            found = dub[0]
            dynamic = int(dub[1])
            anl.addAnalysis(found)
            currentScore = anl.scoreSong()
            print ''
            print "<"+str(found)+" heard, current score "+str(currentScore)+"% >"
            self.writeOut(str(counter), str(note)+','+str(found)+','+str(dynamic)+','+str(tempo)+'bps'+','+str(currentScore))
            sml.advanceSegment()
            counter += 1
        
        '''
        if os.getenv(self.var, 'CONT') == 'STOP':
            message = "<song interrupted>"
            print message
            os.environ[self.var] = ''
        '''
        if listy:
            message = "<song interrupted>"
            print message
            #self.writeOut("message", message)
        else:
            total = anl.scoreSong()
            print "<total score is "+str(total)+"% >"
            #self.writeOut("score", str(total))
        
        #sml.resetSampler()
        
        
        stream.stop_stream()
        stream.close()
        pyaud.terminate()
        return


    def interrupter(self, listy):
        raw_input()
        listy.append(True)

##og = organizer()
##og.main()