from django.shortcuts import render
from .models import Cart
from.serializers import W_Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class Cartview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Cart.objects.filter(user=request.user)
        return Response(W_Cart(items, many=True).data)



class Add_Cart(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {
                    "success": False,
                    "message": " you are not logged in"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        product_id = request.data.get("product")
        item, created = Cart.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )
        if not created:
            item.qauntity += 1
            item.save()
        return Response(
            {
                "success": True,
                "message": "Product added to cart",
                "data": W_Cart(item).data
            },
            status=status.HTTP_200_OK
        )



class Decrease_Cart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get("product")
        item = Cart.objects.filter(
            user=request.user,
            product_id=product_id).first()

        if not item:
            return Response({"detail": "Item not found"}, status=404)

        if item.qauntity > 1:
            item.qauntity -= 1
            item.save()
        else:
            item.delete()

        return Response({"message": "updated"})

class delete_Cart(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        product_id = request.query_params.get("product")
        Cart.objects.filter(
            user=request.user,
            product_id=product_id).delete()
        return Response({"message": "removed"})

