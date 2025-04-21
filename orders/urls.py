# orders/urls.py
from django.urls import path
from .views import create_order_view,inventory_by_model_view

urlpatterns = [
    path('new/', create_order_view, name='create_order'),
    path('inventory/by-model/<str:model>/', inventory_by_model_view, name='inventory_by_model'),
]
