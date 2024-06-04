from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view 
from rest_framework.response import Response

from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        querryset = Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]
        serializer = ProductSerializer(querryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST': 
        # serializer = ProductSerializer(data = request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('OK')

        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        serializer = ProductSerializer(data = request.data)
        # data validation
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      

@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request,id): 
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':          
        serializer = ProductSerializer(product)
        return Response(serializer.data) 
    elif request.method == 'PUT':
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if product.orderitem_set.count()>0:
            return Response({'error':'This product can not be deleted because it is associated with Order Item.'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status= status.HTTP_204_NO_CONTENT) 
    

@api_view(['GET', 'POST'])    
def collections_list(request):
    if request.method == 'GET':
        querryset = Collection.objects.all()
        serializer = CollectionSerializer(querryset, many=True, context = {'request': request})
        return Response(serializer.data, status= status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data= request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status= status.HTTP_201_CREATED)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT','DELETE'])
def collection_details(request,id):
    collection = get_object_or_404(Collection, pk=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status= status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error':'This Collection can not be deleted because it has associated products'}, 
                            status= status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response({'message': f'Collection {collection.title} Deleted'},status.HTTP_204_NO_CONTENT)
    
def orders(request):
    return HttpResponse('Orders') 
