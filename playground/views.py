from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F

from store.models import Product
# Create your views here.


def say_hello(request):
    query_set = Product.objects.all()
    for product in query_set:
        print(product)
      
    try:
        product1 = Product.objects.get(pk=0)
        # print(product1)
    except ObjectDoesNotExist:
        print("That product does not exist")
        
    querryset = Product.objects.filter(unit_price__range = (20,30))
    # print(querryset)
    
    querryset = Product.objects.filter(category__id= 3) # select products where category = 3
    
    querryset = Product.objects.filter(title__icontains = 'coffee') # select * products where title contaoins coffee
    
    querryset = Product.objects.filter(last_update__year__range = (2018,2020)) # select * products where last update is in range (2018,2020)
    
    querryset = Product.objects.filter(description__isnull = True) # select * products where description is null
    
    # Complex Loopkups (Filtering based on morethan one condition ) using Q object
    querryset = Product.objects.filter(category_id =3, title__icontains = 'coffee') # select * products where category_id = 3 and in their title contains 'coffee'
    querryset = Product.objects.filter(category_id =3).filter(title__icontains = 'coffee') #same as the above line
    
    #Using OR Operator
    querryset = Product.objects.filter(Q(category_id = 3) | Q(title__icontains = 'Coffe'))
    
    querryset = Product.objects.filter(Q(category_id = 3) | ~Q(title__icontains = 'Coffe')) #Negate the second argument
    
    #Referencing the objects using F Object
    
    querryset = Product.objects.filter(category_id = F('inventory')) # Display all the products with inventory that equals to category
    
    product = Product.objects.order_by('unit_price')[0] # Display first product ascendingly on unit price
    product = Product.objects.aearliest('unit_price') # Same as above
    product = Product.objects.latest('unit_price') # Display the last product ascendingly on unit price
    product = Product.objects.order_by('-unit_price') # Display products Descendingly on unit price
     
    return render(request, 'hello_world.html',{'title':'Mr Phase', 'products': list(querryset)})