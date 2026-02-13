from rest_framework import serializers
from order.models import OrderItem,Order


class Dashboard_Serializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    blocked_users = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    username = serializers.CharField(source="order.user.username", read_only=True)
    

    class Meta:
        model = OrderItem
        fields = ["id","username","product_name","quantity","price",]



class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id","user_email","total","created_at","items",]

