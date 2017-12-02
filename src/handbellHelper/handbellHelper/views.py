from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from subprocess import Popen
import os

def app(request):
    bunk = ''
    if request.method == 'POST':
        button = request.POST.get('button', None)
        if button == 'play':
            select = request.POST.get('select', None)
            proc = Popen(['python', '/home/pi/capstone/src/main.py', '-play', select])
            print proc
        elif button == 'stop':
            f = open("./../write.csv","r")
            output = f.read()
            f.close()
            bunk = output
    with open("./../sheet/songs.txt", "r") as f:
        songs = f.read().split('\n')
    return render(request, 'forms.html', {'song_dicts':songs, 'bunk':bunk})