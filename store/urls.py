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
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet)

#chird router 
product_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
#By setting loopup to product means that we gonna have product_pk
product_router.register('review', views.ReviewViewSet, basename='product_review')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup = 'cart') #with this we gona have cart_pk in our CartItemsViewSet
carts_router.register('items', views.CartItemsViewSet, basename='cart-items')
# pprint(router.urls)
urlpatterns = [
     path('', include(router.urls+product_router.urls+carts_router.urls)),
     
     # path('', include(router.urls+carts_router.urls))
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
