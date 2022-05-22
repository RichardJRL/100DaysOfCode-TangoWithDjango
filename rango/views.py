from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    "Rango says hey there partner! For more information about Rango please click on <a href='/rango/about/'>About</a>"
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'RichardJRL'}
    return render(request, 'rango/about.html', context=context_dict)
