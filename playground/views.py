from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def claculate():
    x = 3
    y = 5
    return x+y

def say_hello(request):
    x = claculate()
    y = 100
    return render(request, 'hello_world.html',{'title':'Mr Phase'})