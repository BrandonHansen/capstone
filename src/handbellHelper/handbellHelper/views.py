from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse


def app(request):
    
    f = open("./handbellHelper/templates/index.html", "r")
    output = f.read()
    f.close()
    return HttpResponse(output)