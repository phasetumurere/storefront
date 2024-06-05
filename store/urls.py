from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('orders/', views.orders),
    path('products/<int:id>', views.ProductDetails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:id>', views.collection_details, name= 'collection-details'),
    
]
