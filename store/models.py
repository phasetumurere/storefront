from django.db import models
from django.core.validators import MinValueValidator

from django.conf import settings
from django.contrib import admin

import rest_framework
from uuid import uuid4
from core.models import User
from storefront.settings import AUTH_USER_MODEL



# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL,related_name='+')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null = True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(2)])
    last_update = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products') 
    # Models. protct, if we accidentally delete collection we don't hae to delete all the products in that category
    promotions = models.ManyToManyField(Promotion, blank=True)

    # Displaying the list of products intead of default objects in Admin panel.
    def __str__(self):
        return self.title
    
    #Sort products in Admin panel
    class Meta:
        ordering = ['title']
    
    
class Customer(models.Model):
    
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MBEMERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MBEMERSHIP_GOLD, 'Gold')
    ]
    #Removed just because of we're using user from the admin
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length= 30)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length= 1, 
                                  choices = MEMBERSHIP_CHOICES, 
                                  default=MEMBERSHIP_SILVER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' 
    
    class Meta:
        ordering = ['user__first_name','user__last_name']
        permissions = [('view_history', 'Can View History')]
    
    
class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_COMPLETED, 'Completed'),
        (PAYMENT_FAILED,'Failed'),
        (PAYMENT_PENDING,'Pending'),
    ]
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, 
                                      choices = PAYMENT_STATUS_CHOICES,
                                      default = PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
    #if we delete the customer we don't delete Orders because the orders are our sells so they don't have to be deleted
    
    #Creating Custom Permissions for Order (Cancel the Order)
    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel the order')]
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete= models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)
    
    
    #One to One relationship between Customer and Address
class Address(models.Model):
    city = models.CharField(max_length= 255)
    street = models.CharField(max_length= 255)
    customer = models.OneToOneField(Customer, 
                                    on_delete = models.CASCADE, 
                                    primary_key = True)
    
    
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') #items from cartitem_set
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]) #PositiveSmallIntegerField
    
    class Meta:
        unique_together = [['cart', 'product']]
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= 'reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    