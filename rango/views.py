from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "Rango says hey there partner! For more information about Rango please click on <a href='/rango/about/'>About</a>")


def about(request):
    return HttpResponse(
        "Rango says here is the about page. To get back to the Rango homepage, click on <a href='/rango/'>Index</a>")
