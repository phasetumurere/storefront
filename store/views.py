from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view 
from rest_framework.response import Response

from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        querryset = Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]
        serializer = ProductSerializer(querryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':        
        serializer = ProductSerializer(data = request.data)
        # data validation
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('OK')
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('OK')

        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    
    