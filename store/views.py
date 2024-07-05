from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend #Perform filters (any field in any model)


from rest_framework import status
from rest_framework.decorators import api_view, action 
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin #Create a re useable codes
from rest_framework.response import Response
from rest_framework.views import APIView #Class based Views
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from storefront.settings import REST_FRAMEWORK
from store.admin import OrderModelAdmin
from .default_pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, OrderItem, Product, Review, Customer
from .serializers import (AddCartItemSerializer, CartItemsSerializer, CartSerializer,
    CollectionSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, CustomerSerializer)


# Product View set
class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # filterset_fields = ['category_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    # search_fields = ['title', 'description', 'category__title'] # Search in related data
    ordering_fields = ['unit_price', 'last_update']
    # pagination_class = PageNumberPagination #Pagination Locally
    pagination_class = DefaultPagination
    

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')
    #     if category_id is not None:
    #         queryset = queryset.filter(category_id = category_id)
    #     return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error':'This product can not be deleted because it is associated with Order Item.'},
                            status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request,pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitem_set.count()>0:
    #         return Response({'error':'This product can not be deleted because it is associated with Order Item.'},
    #                         status= status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response({'message':f'Product {product.title} Have Deleted Succesifully!'}, status= status.HTTP_204_NO_CONTENT) 
     

#Generic Views
# class ProductList(ListCreateAPIView):
#     # def get_queryset(self):
#     #     return Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]    
   
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     # queryset = Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]
#     queryset = Product.objects.all().order_by('-unit_price')[:4]
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
  
#   ###### Product List Class & Function Based Views ######  
# # {
# #  # # Class based Views
# # # class ProductLists(APIView):
# # #     def get(self, request):
# # #         querryset = Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]
# # #         serializer = ProductSerializer(querryset, many=True, context={'request': request})
# # #         return Response(serializer.data)
    
# # #     def post(self, request):
# # #         serializer = ProductSerializer(data = request.data)
# # #         # data validation
# # #         serializer.is_valid(raise_exception=True)
# # #         serializer.validated_data
# # #         serializer.save()
# # #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
# # # Create your views here.
# # #Function based Views
# # # @api_view(['GET', 'POST'])
# # # def product_list(request):
# # #     if request.method == 'GET':
# # #         querryset = Product.objects.all().select_related('category').all().order_by('-unit_price')[:4]
# # #         serializer = ProductSerializer(querryset, many=True, context={'request': request})
# # #         return Response(serializer.data)
# # #     elif request.method == 'POST': 
# # #         # serializer = ProductSerializer(data = request.data)
# # #         # if serializer.is_valid():
# # #         #     serializer.validated_data
# # #         #     return Response('OK')

# # #         # else:
# # #         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
# # #         serializer = ProductSerializer(data = request.data)
# # #         # data validation
# # #         serializer.is_valid(raise_exception=True)
# # #         serializer.validated_data
# # #         serializer.save()
# # #         return Response(serializer.data, status=status.HTTP_201_CREATED)
     
# # }

#Product Details Generic View
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     # def get_queryset(self):
#     #     return Product.objects.all()
#     queryset = Product.objects.all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#     serializer_class = ProductSerializer
    
#     def delete(self, request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count()>0:
#             return Response({'error':'This product can not be deleted because it is associated with Order Item.'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'message':f'Product {product.title} Have Deleted Succesifully!'}, status= status.HTTP_204_NO_CONTENT) 
     

##### Product Details Class & Function Based Views #####
# {
#    # Product Details Class based View
# # class ProductDetails(APIView):

# #     def get(self, request,id):
# #         product = get_object_or_404(Product, pk=id)
# #         serializer = ProductSerializer(product)
# #         return Response(serializer.data)  
    
# #     def put(self, request,id):
# #         product = get_object_or_404(Product, pk=id)
# #         serializer = ProductSerializer(product, data = request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
    
# #     def delete(self, request,id):
# #         product = get_object_or_404(Product, pk=id)
# #         if product.orderitem_set.count()>0:
# #             return Response({'error':'This product can not be deleted because it is associated with Order Item.'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
# #         product.delete()
# #         return Response({'message':f'Product {product.title} Have Deleted Succesifully!'}, status= status.HTTP_204_NO_CONTENT) 
         
   
# # Product Details Function based View     
# # @api_view(['GET', 'PUT', 'DELETE'])
# # def product_details(request,id): 
# #     product = get_object_or_404(Product, pk=id)
# #     if request.method == 'GET':          
# #         serializer = ProductSerializer(product)
# #         return Response(serializer.data) 
# #     elif request.method == 'PUT':
# #         serializer = ProductSerializer(data = request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
# #     elif request.method == 'DELETE':
# #         if product.orderitem_set.count()>0:
# #             return Response({'error':'This product can not be deleted because it is associated with Order Item.'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
# #         product.delete()
# #         return Response({'message':f'Product {product.title} Have Deleted Succesifully!'}, status= status.HTTP_204_NO_CONTENT) 
    
# }
 
 
# Collection Viewset
class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer 
       
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):

        if Product.objects.filter(category_id = kwargs['pk']).count() > 0:
            
            return Response({'error':'This Collection can not be deleted because it has associated products'}, 
                            status= status.HTTP_400_BAD_REQUEST)
                    
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.product_set.count() > 0:
    #         return Response({'error':'This Collection can not be deleted because it has associated products'}, 
    #                         status= status.HTTP_400_BAD_REQUEST)
    #     collection.delete()
    #     return Response({'message': f'Collection {collection.title} Deleted'},status.HTTP_204_NO_CONTENT)
     

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all().filter(product_id = self.kwargs['product_pk'])
    
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(GenericViewSet,
                  CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all() #Gona have multiple Items 
    serializer_class = CartSerializer
    

class CartItemsViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer  
          
        return CartItemsSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']} # I'm going to need this cart_id in Serializer by self.context
   


class CustomerViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else: return [IsAuthenticated()]
    
    @action(detail=False, methods= ['GET', 'PUT'])#,  permission_classes = [IsAuthenticated], 
    def me(self, request):
        if request.user.is_authenticated:
            (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
            if request.method == 'GET':            
                serializer = CustomerSerializer(customer)
                return Response(serializer.data)
            elif request.method == 'PUT':
                serializer = CustomerSerializer(customer, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else: return Response(status=status.HTTP_401_UNAUTHORIZED)
        # return Response(request.user.id)
    
    
    
# Collection Generic Views
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}

##### Collection List Class & Function Based Views #####
# {
#    # CollectionList Class Based View
# # class CollectionLists(APIView):
# #     def get(self, request):
# #         querryset = Collection.objects.all()
# #         serializer = CollectionSerializer(querryset, many=True, context = {'request': request})
# #         return Response(serializer.data, status= status.HTTP_200_OK)
    
# #     def post(self, request):
# #         serializer = CollectionSerializer(data= request.data)
# #         # if serializer.is_valid():
# #         #     serializer.save()
# #         #     return Response(serializer.data, status= status.HTTP_201_CREATED)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
               
# # Collection Function Base View        
# # @api_view(['GET', 'POST'])    
# # def collections_list(request):
# #     if request.method == 'GET':
# #         querryset = Collection.objects.all()
# #         serializer = CollectionSerializer(querryset, many=True, context = {'request': request})
# #         return Response(serializer.data, status= status.HTTP_200_OK)
# #     elif request.method == 'POST':
# #         serializer = CollectionSerializer(data= request.data)
# #         # if serializer.is_valid():
# #         #     serializer.save()
# #         #     return Response(serializer.data, status= status.HTTP_201_CREATED)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
   
 
# }

# Collection Details Generic View
# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#     # def get_queryset(self):
#     #     return Collection.objects.all()
#     # def get_serializer_class(self):
#     #     return CollectionSerializer
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.product_set.count() > 0:
#             return Response({'error':'This Collection can not be deleted because it has associated products'}, 
#                             status= status.HTTP_400_BAD_REQUEST)
#         collection.delete()
#         return Response({'message': f'Collection {collection.title} Deleted'},status.HTTP_204_NO_CONTENT)
     
##### Collection Details Class & Function Based Views #####
# {
#   # Collection Details Class based View
# # class CollectionDetails(APIView):
# #     def get(self, request, id):
# #         collection = get_object_or_404(Collection, pk=id)
# #         serializer = CollectionSerializer(collection)
# #         return Response(serializer.data, status= status.HTTP_200_OK)
    
# #     def put(self, request, id):
# #         serializer = CollectionSerializer(data= request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
    
# #     def delete(self, request, id):
# #         collection = get_object_or_404(Collection, pk=id)
# #         if collection.product_set.count() > 0:
# #             return Response({'error':'This Collection can not be deleted because it has associated products'}, 
# #                             status= status.HTTP_400_BAD_REQUEST)
# #         collection.delete()
# #         return Response({'message': f'Collection {collection.title} Deleted'},status.HTTP_204_NO_CONTENT)
     

# # @api_view(['GET', 'PUT','DELETE'])
# # def collection_details(request,id):
# #     collection = get_object_or_404(Collection, pk=id)
# #     if request.method == 'GET':
# #         serializer = CollectionSerializer(collection)
# #         return Response(serializer.data, status= status.HTTP_200_OK)
# #     elif request.method == 'PUT':
# #         serializer = CollectionSerializer(data= request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.validated_data
# #         serializer.save()
# #         return Response(serializer.data, status= status.HTTP_201_CREATED)
# #     elif request.method == 'DELETE':
# #         if collection.product_set.count() > 0:
# #             return Response({'error':'This Collection can not be deleted because it has associated products'}, 
# #                             status= status.HTTP_400_BAD_REQUEST)
# #         collection.delete()
# #         return Response({'message': f'Collection {collection.title} Deleted'},status.HTTP_204_NO_CONTENT)
   
# }
   
def orders(request):
    return HttpResponse('Orders') 
