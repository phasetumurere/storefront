import django.db
import django.db.models
from rest_framework import serializers
from .models import Cart, Collection, Product, Review, CartItem, Customer, Order, OrderItem
from decimal import Decimal

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length= 255)
    
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
        
    product_count = serializers.SerializerMethodField(method_name='products_associated_count')
    # product_count = serializers.IntegerField(read_only=True)
    

    def products_associated_count(self, collection: Collection):
        return collection.product_set.count()


# class ProductSerializer(serializers.Serializer):
class ProductSerializer(serializers.ModelSerializer):
    # ####### Modal Serialization###
    class Meta:
        model = Product
        # fields = ['id', 'title', 'slug', 'description', 'inventory','category', 'price', 'price_with_tax', 'associated_orders']
        fields = ['id', 'title', 'slug', 'description', 'inventory','category', 'price', 'price_with_tax']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    # associated_orders = serializers.SerializerMethodField(method_name= 'order_count')
    # # # collection = serializers.PrimaryKeyRelatedField(queryset= Collection.objects.all(), source = 'category') #First way to Serialize a Relationship by it's ID
    # reviews = serializers.PrimaryKeyRelatedField(queryset= Review.objects.all()) #First way to Serialize a Relationship by it's ID
    # category = serializers.StringRelatedField() #Second way to Serialize a Relationship by it's name
    # reviews = serializers.StringRelatedField() #Second way to Serialize a Relationship by it's name
    # # collection = CollectionSerializer(source='category') ## Second way to Serialize a Relationship by it's object Instatiation
        
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name= 'collection-details'
    #     # source='category'
    # )
    
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class ReviewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
            
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
    
class CartItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    items = CartItemsSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart:Cart):
        # [item.quantity * item.product.unit_price for item in cart.items.all()] #with this expression we get the list of totals now we need to sum all of them
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price']
        
        
class AddCartItemSerializer(serializers.ModelSerializer):    
    product_id = serializers.IntegerField()
        
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
        
    def validate_product_id(self, Value):
        if not Product.objects.filter(pk =Value).exists():
            raise serializers.ValidationError(f"No Product with id {Value} found")
        return Value
        
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id = product_id)
            # Update the Cart or CartItem 
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create a new CartItem 
            self.instance = CartItem.objects.create(cart_id = cart_id,
                                    **self.validated_data)
        return self.instance
        

class UpdateCartItemSerializer(serializers.ModelSerializer):       
    class Meta:
        model = CartItem
        fields = ['quantity']
        
        
class CustomerSerializer(serializers.ModelSerializer):  
    user_id = serializers.IntegerField(read_only = True)  
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'membership', 'birth_date']

class OderItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']        

class OrderSerializer(serializers.ModelSerializer):
    items = OderItemsSerializer(many=True)
    class Meta:
        model = Order
        fields =['id', 'customer', 'placed_at', 'payment_status', 'items']
        
        
class SaveOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def save(self, **kwargs):
        print(self.validated_data['cart_id'])
        print(self.context['user_id'])
        
        (customer, created) = Customer.objects.get_or_create(user_id =  self.context['user_id'])
        return Order.objects.create(customer = customer)
    
          

    # def order_count(self, product: Product):
    #     return product.orderitem_set.count()
    
    
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
    
