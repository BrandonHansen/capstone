import numpy
import pyaudio
import analyse
import math

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

index = 0

for i in range(pyaud.get_device_count()):
  dev = pyaud.get_device_info_by_index(i)
  if dev['name'] == 'USB PnP Sound Device: Audio (hw:1,0)':
     index = i
     break
  #print((i,dev['name'],dev['maxInputChannels']))


# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 4 is a USB microphone
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = i,
    input = True,
    frames_per_buffer = 1024)

pitch_array=[]
while True:
    # Read raw microphone data
    rawsamps = stream.read(1024, exception_on_overflow = False)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    vol_sample=analyse.loudness(samps)
    pitch_sample=analyse.musical_detect_pitch(samps)
    print vol_sample, pitch_sample
    if pitch_sample != None:
        pitch_array.append(pitch_sample)
    print avg(pitch_array)
