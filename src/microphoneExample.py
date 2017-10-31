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
pitches.recordPitch(['A','C','D'])


print pitches.set

#exit(0)

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 4 is a USB microphone
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = 2,
    input = True)

tempo = comp.getTempo()
song = comp.getSong()
score = []

print "start"

print "5"
time.sleep(1)
print "4"
time.sleep(1)
print "3"
time.sleep(1)
print "2"
time.sleep(1)
print "1"
time.sleep(1)

for beat in song:
    current = time.clock()
    running = []
    print beat
    while time.clock() - current  < tempo:
        rawsamps = stream.read(1024)
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        note_in = analyse.musical_detect_pitch(samps)
        if note_in != None:
            running.append(note_in)
    record = numpy.average(running)
    if pitches.set[beat][0]-pitches.set[beat][1] <= record <= pitches.set[beat][0]+pitches.set[beat][1]:
        score.append(1)
    else:
        score.append(0)

print "finished"

print sum(score)/len(score)

'''
while True:
    # Read raw microphone data
    rawsamps = stream.read(1024)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
'''