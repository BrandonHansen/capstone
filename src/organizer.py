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

class organizer:

    inl = initializer.initializer("songs.txt", "pitch.txt", "sheet")
    songs = {}
    pitch = {}
    #sample analyzer or samplyzer

    def __init__(self):
        #song = {'l':"test", 't':0.1, 'n':['A','B','C','D','E']}
        self.songs = self.inl.getSongs()
        self.pitch = self.inl.getPitches()

    def printOptions(self):
        
        print "help > display this help list"
        print "song > display songs in library"
        print "play > play a song in library"
        print "exit > close this program"

    def printLibrary(self):
        
        for song in self.songs:
            print "Name> "+song

    def main(self):


        display = ">>Welcome to Hand Bell Helper, choose an option 'help'>> "

        inp = "continue"

        while inp != 'exit':
            
            inp = raw_input(display)
            elements = inp.split(' ')
            if inp == 'help':
                self.printOptions()
            elif inp == 'song':
                self.printLibrary()
            elif elements[0] == 'play':
                if len(elements) < 2:
                    title = raw_input("Which song> ")
                else:
                    title = elements[1]
                if self.songs[title] != None:
                    self.startPlaying(self.songs[title])
                else:
                    print "<song dos not exist>"
            elif inp == 'exit' or inp == 'quit':
                #stream.stop_stream()
                #stream.close()
                #pyaud.terminate()
                pass
            else:
                print "<not an option (:-/ >"

            display = ">> "


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
            print "--> microphone not detected"
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
        print "\n<starting in>"
        while count > 0:
            time.sleep(1)
            sys.stdout.write(str(count)+" ")
            sys.stdout.flush()
            count -= 1
        time.sleep(1)
        print ''

        for note in notes:
            print "<play note "+str(note)+" >"
            current = time.clock()            
            tracker = int(tempo)
            while (time.clock() - current < tempo) and (not listy):
                # Read raw microphone data
                rawsamps = stream.read(1024, exception_on_overflow = False)
                # Convert raw data to NumPy array
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
                # Show the volume and pitch
                volume = analyse.loudness(samps)
                pitch = analyse.musical_detect_pitch(samps)
                #print (volume)*-1, pitch
                sml.appendSegment(pitch, (volume)*-1)
                '''
                if ((time.clock() - current) - tempo) < tracker:
                    sys.stdout.write(str(tracker)+" ")
                    sys.stdout.flush()
                    tracker -= 1
                '''
            sys.stdout.flush()
            found  = anl.analyzeSegment(sml.getCurrentSegment())
            anl.addAnalysis(found)
            print ''
            print "<heard "+str(found)+" >"
            sml.advanceSegment()
        
        if listy:
            print "<song interrupted>"
        else:
            total = anl.scoreSong()
            print "<total score is "+str(total)+"% >"
        
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