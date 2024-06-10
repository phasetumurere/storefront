from django.db import models
from django.core.validators import MinValueValidator



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
    category = models.ForeignKey(Collection, on_delete=models.PROTECT) 
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
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length= 30)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length= 1, 
                                  choices = MEMBERSHIP_CHOICES, 
                                  default=MEMBERSHIP_SILVER)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}' 
    
    class Meta:
        ordering = ['first_name','last_name']
    
    
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
    
    #Sorting the customer
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.PROTECT)
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
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= 'reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    