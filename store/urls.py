from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter,DefaultRouter
from pprint import pprint

from rest_framework_nested import routers

from . import views

#Parent router
router = routers.DefaultRouter() # By using this Defaut 
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewset)
router.register('carts', views.CartViewSet)

#chird router 
product_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
#By setting loopup to product means that we gonna have product_pk
product_router.register('review', views.ReviewViewSet, basename='product_review')
# pprint(router.urls)
urlpatterns = [
     path('', include(router.urls+product_router.urls)),
     path('orders/', views.orders) ,
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
