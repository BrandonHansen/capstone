import organizer
import sys

input1 = sys.argv[1]
if len(sys.argv) > 2:
    input2 = sys.argv[2]
else:
    input2 = None

og = organizer.organizer()
og.cmd_interface(input1, input2, 'NONE')
