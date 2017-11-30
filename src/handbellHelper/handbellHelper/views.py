from django.shortcuts import render
from django.http import HttpResponse

def app(request):
    f = open("./../score.txt","r")
    output = f.read()
    f.close()
    return HttpResponse(output)
