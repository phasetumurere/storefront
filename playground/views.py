from django.forms import DecimalField
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F, Func, Value, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Sum, Avg, Min, Max, Count
from store.models import Product, OrderItem, Order, Customer, Collection
from django.db import transaction # Saving OrderItem since it has a relationship between them

#Imports for generic relationships
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from tags.models import TaggedItemManager



# def say_hello(request):
#     # query_set = Product.objects.all()
#     # for product in query_set:
#     #     print(product)
      
#     # try:
#     #     product1 = Product.objects.get(pk=0)
#     #     # print(product1)
#     # except ObjectDoesNotExist:
#     #     print("That product does not exist")
        
#     # querryset = Product.objects.filter(unit_price__range = (20,30))
#     # # print(querryset)
    
#     # querryset = Product.objects.filter(category__id= 3) # select products where category = 3
    
#     # querryset = Product.objects.filter(title__icontains = 'coffee') # select * products where title contaoins coffee
    
#     # querryset = Product.objects.filter(last_update__year__range = (2018,2020)) # select * products where last update is in range (2018,2020)
    
#     # querryset = Product.objects.filter(description__isnull = True) # select * products where description is null
    
#     # # Complex Loopkups (Filtering based on morethan one condition ) using Q object
#     # querryset = Product.objects.filter(category_id =3, title__icontains = 'coffee') # select * products where category_id = 3 and in their title contains 'coffee'
#     # querryset = Product.objects.filter(category_id =3).filter(title__icontains = 'coffee') #same as the above line
    
#     # #Using OR Operator
#     # querryset = Product.objects.filter(Q(category_id = 3) | Q(title__icontains = 'Coffe'))
    
#     # querryset = Product.objects.filter(Q(category_id = 3) | ~Q(title__icontains = 'Coffe')) #Negate the second argument
    
#     # #Referencing the objects using F Object    
#     # querryset = Product.objects.filter(category_id = F('inventory')) # Display all the products with inventory that equals to category
    
#     # product = Product.objects.order_by('unit_price')[0] # Display first product ascendingly on unit price
#     # product = Product.objects.aearliest('unit_price') # Same as above
#     # product = Product.objects.latest('unit_price') # Display the last product ascendingly on unit price
#     # product = Product.objects.order_by('-unit_price') # Display products Descendingly on unit price
#     # querryset = Product.objects.all().order_by('-unit_price')[:5] #Display first 5 objects 
#     # querryset = Product.objects.all().values('unit_price','inventory', 'title') #Selecting certain Features
#     # querryset = Product.objects.all().values('unit_price','inventory', 'title', 'category__title') #Selecting certain Features but also from another table
#     # querryset = Product.objects.all().order_by('title').filter(category__title = 'beauty')
    
#     # # Selecting the products that have been ordered (From Product table to OrderItem table)
#     # # and display only those products that have been ordered then solt them by their title
#     # OrderedItems = OrderItem.objects.values('product_id').distinct()
#     # querryset = Product.objects.all().filter(id__in=OrderedItems).order_by('title')
#     # # End of the task
    
#     # ## Selecting a related Objects
#     # querryset = Product.objects.select_related('category').all()
    
#     # querryset = Product.objects.prefetch_related('promotions').select_related('category').all()
    
#     # OrderQuerryset = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('-placed_at')[:5]

#     # products = Product.objects.aggregate(count = Count('id'))
#     # categories = Product.objects.filter(category = 4).aggregate(count = Count('id'))
    
#     # return render(request, 'hello_world.html',{'title':'Mr Phase',
#     #                                            'orders': list(OrderQuerryset)})
    
#     # customer_fullnames = Customer.objects.annotate(fullnames = Func(F('first_name'), 
#     #                                                                 Value(' '), F('last_name'), 
#     #                                                                 function='CONCAT'))
#     # querryset = Customer.objects.annotate(orders_count = Count('order'))
    
    
#     # # customer_querryset = Customer.objects.all()[:5]
#     # customer_and_orders = Order.objects.all()
    
#     discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field= DecimalField())
#     querryset = Product.objects.annotate(discounted_prices = discounted_price)
    
#     return render(request, 'hello_world.html', {'title':'Mr Phase',                                             
#                                                 # 'customer_fullnames': customer_fullnames,
#                                                 # 'products_count': products, 
#                                                 # 'customer_order_count': querryset,
#                                                 # 'fourth_category_products_count': categories,
#                                                 # 'customers': customer_querryset,
#                                                 # 'customers_and_order':customer_and_orders
#                                                 })


def generic_relationship(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)
    
    querry_set = Product.objects.all()
    list(querry_set)
    
    # # Create a new Collection
    # collection = Collection()
    # collection.title = 'Mododka'
    # collection.featured_product = Product(pk=1)
    # collection.save()
    
    #Updating Collection
    # collection = Collection.objects.get(pk=11)
    # Collection.objects.filter(pk=6).update(featured_product=1)
    
    # # Delete the collection
    # Collection.objects.get(pk=12).delete()
    
    ############### Saving the data let say that want to save Order item but also saving order ###########
    
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()
        
        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
    
    return render(request, 'hello_world.html', {'tags': list(queryset)})
