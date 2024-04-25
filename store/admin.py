from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Count

from django.urls import reverse
from django.utils.html import format_html
from urllib.parse import urlencode



from . import models 

##### Overriding the Base Querryset: let say we want to count every product in the collection
##### Remember that we don't have this field (Product_count) in collections table
@admin.register(models.Collection)
class CollectionAdminModel(admin.ModelAdmin):
    list_display = ['title','products_count']
    
    @admin.display(ordering= 'products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')+
               '?'+urlencode(
                   {'category__id': str(collection.id)}
                   )) # Url for the clicked products
        # url = f'product/?collection_id={5}'
        if collection.products_count == 0:
            url = 0
            return url
        return format_html('<a href="{}">{}', url, collection.products_count)
             
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
            )
      

# Register your models here.
@admin.register(models.Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'category_title', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['category']
    
    def category_title(self, product):
        return product.category.title
    
    @admin.display(ordering= 'inventory')
    def inventory_status(self, product):
        if product.inventory <=10:
            return 'Low'
        else:
            return 'Ok'
    

@admin.register(models.Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'id','orders_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    
    @admin.display(ordering='first_name')
    def orders_count(self, customer):

        url = (reverse('admin:store_order_changelist')+
        '?'+urlencode({'customer_id': str(customer.id)})) 
        if customer.order_set.count()==0: #if no order then no need of a clickable link to the order's made bya that customer
            url = 0  
            return url            
        else:
            return format_html('<a href="{}">{}', url, customer.order_set.count())
    #order_set attribute is automatically created by Django when you define a foreign key from Order to Customer
    
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         orders_count = Count('order')
    #         )
 
    
@admin.register(models.Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_select_related = ['customer']  
    list_per_page = 10
    