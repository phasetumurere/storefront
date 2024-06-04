from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('orders/', views.orders),
    path('products/<int:id>', views.product_details),
    path('collections/', views.collections_list),
    path('collections/<int:id>', views.collection_details, name= 'collection-details'),
    
]
