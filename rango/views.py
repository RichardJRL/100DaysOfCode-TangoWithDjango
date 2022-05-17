from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "Rango says hey there partner! For more information about Rango please click <a href='/rango/about/'>here</a>")


def about(request):
    return HttpResponse(
        "Rango says here is the about page. To get back to the Rango homepage, click  <a href='/rango/'>here</a>")
