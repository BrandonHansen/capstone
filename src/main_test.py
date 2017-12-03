import organizer
import sys
import os

def mainLoop(og, input_var):
    var = os.getenv(input_var, 'NONE')
    if var == 'NONE':
        sys.exit(0)
    while True:
        var = os.getenv(input_var, 'EXIT')
        if var == 'EXIT':
            os.environ[input_var] = ''
            sys.exit(0)
        elif var == 'STOP':
            os.environ[input_var] = ''
            pass
        elif var.split(',')[0] == "play":
            os.environ[input_var] = ''
            dub = var.split(',')
            if len(dub) == 2:
                og.cmd_interface('-play', dub[1], input_var)
        else:
            os.environ[input_var] = ''
            pass

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        input1 = sys.argv[1]
    else:
        input1 = None
    
    if len(sys.argv) > 2:
        input2 = sys.argv[2]
    else:
        input2 = None
    
    og = organizer.organizer()
    if input1 == '-watch' and input2 != None:
        input_file = input2
        if os.path.exists(input_file):
            mainLoop(og, input_file)
        else:
            print "<input file does not exist>"
    else:
        og.cmd_interface(input1, input2)
        
    sys.exit(0)
