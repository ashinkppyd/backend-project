from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import Order, OrderItem

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({"message": "Cart is empty"}, status=400)

        total = sum(
            item.product.price * item.qauntity
            for item in cart_items
        )

        order = Order.objects.create(
            user=request.user,
            total=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.qauntity,
                price=item.product.price
            )

        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id
        })


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        data = []
        for order in orders:
            data.append({
                "id": order.id,
                "date": order.created_at,
                "total": order.total,
                "items": [
                    {
                        "id": item.product.id,
                        "name": item.product.name,
                        "image": item.product.image, 
                        "quantity": item.quantity,
                    }
                    for item in order.items.all()
                ]
            })

        return Response(data)