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
        fields = ['id', 'title', 'slug', 'description', 'inventory','category', 'price', 'price_with_tax']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    # # # collection = serializers.PrimaryKeyRelatedField(queryset= Collection.objects.all(), source = 'category') #First way to Serialize a Relationship by it's ID
    # category = serializers.StringRelatedField() #Second way to Serialize a Relationship by it's name
    # # collection = CollectionSerializer(source='category') ## Second way to Serialize a Relationship by it's object Instatiation
        
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name= 'collection-details'
    #     # source='category'
    # )
    
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    
    # def password_varidation(self, data):
    #     if data['password']!= data['confirm_password']:
    #         return serializers.ValidationError("Passwords not match")
    #     return data 
    
    
    # ## we can also overlide how    product is created
    # def create(self, validated_data):
    #     product = Product(**validated_data) #Unpack validated data
    #     product.other = 23
    #     product.whatever = "what ever the value"
    #     product.save()
    #     return product
    
    # ## Overlide update product
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.quantity = validated_data.get('quantity')
    #     instance.save()
    #     return instance
    
