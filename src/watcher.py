import subprocess
import time


input_file = "input.txt"
proc = None
count = 0


while True:
    file = open(input_file, 'r+')
    line = file.readline().replace('\n','').replace('\r','')
    if line == '':
        pass
    elif line == 'EXIT':
        file.close()
        open(input_file, 'w').close()
        break
    elif line == 'STOP':
        if proc != None:
            proc.kill()
            proc = None
        file.close()
        open(input_file, 'w').close()
    elif line.split(',')[0] == "play":
        dub = line.split(',')
        if len(dub) == 2:
            song = dub[1]
            proc = subprocess.Popen(['python', '/home/pi/capstone/src/main.py', '-play', song])
            
        file.close()
        open(input_file, 'w').close()