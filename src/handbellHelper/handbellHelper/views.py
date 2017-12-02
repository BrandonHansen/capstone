from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse


def index(request):
    
    f = open("./handbellHelper/templates/index.html", "r")
    output = f.read()
    f.close()
    return HttpResponse(output)

def practice(request):
    
    f = open("./handbellHelper/templates/practice.html", "r")
    output = f.read()
    f.close()
    return HttpResponse(output)