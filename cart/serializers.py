from rest_framework import serializers
from .models import Cart
from products.serializers import W_Products

class W_Cart(serializers.ModelSerializer):
    product = W_Products(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "product", "qauntity"]