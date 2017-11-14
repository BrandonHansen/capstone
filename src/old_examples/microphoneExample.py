import numpy
import pyaudio
import analyse
import time
import songManager
import pitchGetter

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

comp = songManager.songManager(1, [])
comp.readTextForComposition("sheet/test1")

pitches = pitchGetter.pitchGetter({})
#pitches.loadPitch("sheet/test2")
pitches.loadPitch("sheet/test2")#Pitch(['A','C','D'])

#print pyaud.get_device_count, pyaud.get_device_info_by_index

#exit(0)

print pitches.set

#exit(0)

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 4 is a USB microphone
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = 1,
    input = True)

tempo = comp.getTempo()
song = comp.getSong()
score = 0
total = 0

print "starting in"


raw_input("press any key to go")

n = 5
while n > 0:
    print n
    n = n - 1
    time.sleep(1)


for beat in song:
    current = time.clock()
    #running = []
    note = 0
    print beat
    print time.clock()
    while time.clock() - current < tempo:
        rawsamps = stream.read(1024, exception_on_overflow = False)
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        note_in = analyse.musical_detect_pitch(samps)
        if note_in != None and beat != None:
            note = note_in
        #running.append(note_in)
        #record = numpy.average(running)
        if pitches.set[beat][0]-pitches.set[beat][1] <= note <= pitches.set[beat][0]+pitches.set[beat][1]:
            score = score + 1
        total = total + 1
            

print "finished"
print score
print total
print score/total

'''
while True:
    # Read raw microphone data
    rawsamps = stream.read(1024)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
'''
