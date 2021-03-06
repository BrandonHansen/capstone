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
#from matplotlib.cbook import Null

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

    def writeOut(self, data_type, myData):
        finalData = str(data_type) + "," + str(myData)
        headers = {"Content-Type": "application/json"}
        r = requests.put(url='http://127.0.0.1:8080', data=finalData, headers=headers)
        self.wfile.write(data_type+','+myData+'\n')
        #print "Body:   " + r.request.body
        #print "Status: " + str(r.status_code)
        #print "_--_"
        r2 = requests.get(url='http://127.0.0.1:8080')
        #print "Data from GET: " + r2.text

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
            
        
    def web_interface(self):
        
        server_get = None
        server_text = 'NONE'
        
        print '<organizer: loop start>'
        while True:
            
            if server_text == 'EXIT':
                print '<exit>'
                break
            elif server_text != 'NONE' and server_text != '':
                print '<song not NONE,', server_text, '>'
                if self.songs.get(server_text) != None:
                    print '<song in library, start play>'
                    self.startPlaying(self.songs[server_text])
                    print '<song reset ,', server_text, '>'
                server_text = 'NONE'
                server_put = requests.put(url='http://127.0.0.1:8080/song', data = 'NONE')
                print '<reset put>'
                    
            else:
                print '<server get>'
                server_get = requests.get(url='http://127.0.0.1:8080/song')
                print '<server code,', server_get.status_code, '>'
                if server_get.status_code == 200:
                    server_text = server_get.text
                else:
                    server_text = 'NONE'
                print '<song set,', server_text, '>'
                
            print ''
            time.sleep(0.75)
                
               
        self.wfile.close()
        print '<done>'

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
    

        temp_note = 'Rest'
        temp_found = 'Rest'

        counter = 1
        
        currentScore = 0

        for note in notes:
            print "<play note "+str(note)+" >"
            #self.writeOut("note_play", str(note))
            current = time.clock()
            tracker = time.clock()
            count = 5
            sys.stdout.write(str(count)+" ")
            sys.stdout.flush()
            while ((time.clock() - current)*10 < tempo) and (not listy):
                
                if (time.clock() - tracker)*10 > 0.1:    
                    tracker = time.clock()
                    count -= 1
                    message = str(int(count))
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
               
            print ''
            sys.stdout.flush()
            dub  = anl.analyzeSegment(sml.getCurrentSegment())
            found = dub[0]
            if found == None:
                temp_found = 'Rest'
            else:
                temp_found = found
            dynamic = int(dub[1])
            anl.addAnalysis(found)
            currentScore = anl.scoreSong()
            print 'current', currentScore
            #print ''
            #print "<"+str(found)+" heard, current score "+str(currentScore)+"% >"
            if str(note) == 'None':
                temp_note = 'Rest'
            else:
                temp_note = note
            self.writeOut(str(counter), str(temp_note)+','+str(temp_found)+','+str(dynamic)+','+str((1/tempo)*60)+' bpm'+','+str(currentScore))
            sml.advanceSegment()
            counter += 1
        
        self.writeOut(str(counter), 'f')
        headers = {"Content-Type": "application/json"}
        r=requests.put(url='http://127.0.0.1:8080',data='',headers=headers);
        anl.resetAnalyzer()
        
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
