from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view 
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

# Create your views here.

@api_view()
def product_list(request):
    querryset = Product.objects.select_related('category').all()
    serializer = ProductSerializer(querryset, many=True, context={'request': request})
    return Response(serializer.data)


def orders(request):
    return HttpResponse('Orders') 


@api_view()
def product_details(request,id):            
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data) 

@api_view()
def collection_details(request,pk):
    return Response('OK')
    
    