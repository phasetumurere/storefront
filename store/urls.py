from django.urls import path
from . import views

urlpatterns = [
    path('all_products/', views.store_home)
]
