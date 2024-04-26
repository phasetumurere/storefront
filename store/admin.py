from typing import Any
from django.contrib import admin, messages
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
    search_fields =['title']
    
    @admin.display(ordering= 'products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')+
               '?'+urlencode(
                   {'category__id': str(collection.id)}
                   )) # Url for the clicked products
        # url = f'product/?collection_id={5}'
        if collection.product_set.count()== 0:
            url = 0
            return url
        return format_html('<a href="{}">{}', url, collection.product_set.count())
    # collection.products_count == collection.product_set.count()
             
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count = Count('product')
    #         )
    

# Custom Filtering by Inventory
class InventoryFiltering(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [('<10', 'Low'), ('>10', 'Ok')]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
        if self.value()=='>10':
            return queryset.filter(inventory__gt=10)
      

# Register your models here.
@admin.register(models.Product)
class ProductAdminModel(admin.ModelAdmin):
    autocomplete_fields =['category']
    prepopulated_fields = {'slug': ['title']}
    # readonly_fields = ['slug']
    actions = ['clear_inventory'] #Actions to display (pass the name of custom action methos ad a string)
    list_display = ['title','slug', 'unit_price', 'category_title', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['category']
    list_filter = ['category', 'last_update', InventoryFiltering] #Add Custome filter of Inventory
    search_fields = ['title_istartswith']
    
    def category_title(self, product):
        return product.category.title
    
    @admin.display(ordering= 'inventory')
    def inventory_status(self, product):
        if product.inventory <=10:
            return 'Low'
        else:
            return 'Ok'
        
    
    #Create custom Action by default on top there's action of deletting the selected now let create a custom of update Inventory
    @admin.action(description = 'Clear Inventory')
    def clear_inventory(self, request, querryset):
        updated_count = querryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successifully updated.', messages.ERROR) # Every modal admin contains this method for showing the message to the user
        

@admin.register(models.Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'id','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    
    @admin.display(ordering='first_name')
    def orders_count(self, customer):

        url = (reverse('admin:store_order_changelist')+
        '?'+urlencode({'customer_id': str(customer.id)})) 
        if customer.order_set.count()==0: #if no order then no need of a clickable link to the order's made bya that customer
            url = 0  
            return url           
        else:
            return format_html('<a href="{}">{} Orders', url, customer.order_set.count())
    #order_set attribute is automatically created by Django when you define a foreign key from Order to Customer
    
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         orders_count = Count('order')
    #         )
 
 #Editing children using inlines example we want to add new OrderItem (Manage them to an order)
class OrderItemInline(admin.TabularInline): # TabularInline same as StackedInline
    model = models.OrderItem
    autocomplete_fields=['product']
    extra=1
     
 
    
@admin.register(models.Order)
class OrderModelAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    inlines =[OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
    list_select_related = ['customer']  
    list_per_page = 10
    