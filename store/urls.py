from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter,DefaultRouter
from pprint import pprint

from . import views

router = DefaultRouter() # By using this Defaut 
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewset)

# pprint(router.urls)
urlpatterns = [
     path('', include(router.urls)),
     path('orders/', views.orders)   
]
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('products/', views.ProductList.as_view()),
#     path('orders/', views.orders)
#     # path('products/<int:pk>', views.ProductDetails.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>', views.CollectionDetails.as_view())
#     # path('collections/<int:id>', views.collection_details, name= 'collection-details'),# Function Based View
    
# ]
