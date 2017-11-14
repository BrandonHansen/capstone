import numpy
import pyaudio
import analyse
import time
import sampler
import initializer
import thread

class organizer:

    sml = sampler.sampler()
    inl = initializer.initializer("songs.txt", "pitch.txt", "sheet")
    songs = {}
    pitch = {}
    #sample analyzer or samplyzer

    def __init__(self):
        song = {'l':"test", 't':0.1, 'n':['A','B','C','D','E']}
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
                if elements[1] == None:
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
        
        notes = song['n']
        song_length = len(notes)
        tempo = song['t']
        
        
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

        listy = False
        thread.start_new_thread(self.interrupter, (listy,))


        for note in notes:
            print "play note, ", note
            current = time.clock()
            while (time.clock() - current < tempo) and (not listy):
                # Read raw microphone data
                rawsamps = stream.read(1024, exception_on_overflow = False)
                # Convert raw data to NumPy array
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
                # Show the volume and pitch
                volume = analyse.loudness(samps)
                pitch = analyse.musical_detect_pitch(samps)
                print volume, pitch
                self.sml.appendSegment(pitch, volume)
            self.sml.advanceSegment()
        
        time.sleep(2)
        print "results"
        time.sleep(3)
        print self.sml.getSegment(0)
        
        
        stream.stop_stream()
        stream.close()
        pyaud.terminate()


    def interrupter(listy):
        raw_input()
        print "hit"
        listy = True

og = organizer()
og.main()