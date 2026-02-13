from django.urls import path
from .views import Cartview, Add_Cart, Decrease_Cart, delete_Cart


urlpatterns = [
    path("", Cartview.as_view(), name="cart-list"),     
    path("add/", Add_Cart.as_view(), name="cart-add"),  
    path("decrease/", Decrease_Cart.as_view(), name="cart-decrease"),
    path("delete/", delete_Cart.as_view(), name="cart-delete"),
]