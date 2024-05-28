from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length= 255)
    
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


# class ProductSerializer(serializers.Serializer):
class ProductSerializer(serializers.ModelSerializer):
    # ####### Modal Serialization###
    class Meta:
        model = Product
        fields = ['id', 'title', 'collection','price', 'price_with_tax']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    # # # collection = serializers.PrimaryKeyRelatedField(queryset= Collection.objects.all(), source = 'category') #First way to Serialize a Relationship by it's ID
    collection = serializers.StringRelatedField(source='category') #Second way to Serialize a Relationship by it's name
    # # collection = CollectionSerializer(source='category') ## Second way to Serialize a Relationship by it's object Instatiation
        
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name= 'collection-details'
    #     # source='category'
    # )
    
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
