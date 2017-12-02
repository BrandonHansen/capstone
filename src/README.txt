
FILE OUTPUT SPECIFICATIONS
The current output file is no longer score.txt but is write.csv.
The program will do the command specified before closing.
All the while the file will be opened for appending.
If the file can't currently be in the open state for reading please let me know.

Lines in the file are organized as such

<type of data>,<data>,<data>,...,<data>,X\n

The <type of data> specifies what's being written.
The 'X' at the end is their to confirm that a completed line is being read.
The data in between is is the relevant information.

examples:

instance,1527783.67,X
#instance marks the beginning of a new text stream instance

message,<song message>,X
error,--> some erro,X
#generic text return

song,test1,test2,test3,X
#collection of songs in library

count,3,X
count,2,X
count,1,X
#used for the count downs in the original

note_play,B,X
#this is returned to indicate an expect note

note_return,C,67,X
#this is returned to indicate the note percieved by the program and the current song score

score,89,X
#this is to indicate the total song score




FOR RUNNING THE main.py
To run the main.py command return the songs library:

python main.py -song


To run the paly interface:

python main.py -play <name>


To reset the output file:

python main.py -reset

This will make the entire write.csv file empty
