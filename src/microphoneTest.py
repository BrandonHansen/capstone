import numpy
import pyaudio
import analyse

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

for i in range(pyaud.get_device_count()):
  dev = pyaud.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 4 is a USB microphone
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = 2,
    input = True,
    frames_per_buffer = 1024)

while True:
    # Read raw microphone data
    rawsamps = stream.read(1024, exception_on_overflow = False)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
