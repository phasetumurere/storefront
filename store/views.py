from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def store_home(request):
    return render(request, 'all_products.html')