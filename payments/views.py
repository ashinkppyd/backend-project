import hmac
import hashlib
from decimal import Decimal

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from account.authentication import CookieJWTAuthentication
from .Razorpay.razorpay_client import client
from order.models import Order, OrderItem

# stripe.api_key = settings.STRIPE_SECRET_KEY


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def create_payment_intent(request):
   
#     try:
#         amount = request.data.get("amount")

#         if not amount:
#             return Response(
#                 {"error": "Amount is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         intent = stripe.PaymentIntent.create(
#             amount=int(amount),     
#             currency="inr",
#             payment_method_types=["card"],
#             metadata={
#                 "user_id": request.user.id,
#                 "email": request.user.email,
#             },
#         )

#         return Response(
#             {"client_secret": intent.client_secret},
#             status=status.HTTP_200_OK
#         )

#     except Exception as e:
#         return Response(
#             {"error": str(e)},
#             status=status.HTTP_400_BAD_REQUEST
#         )



class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
       
        order = Order.objects.filter(user=request.user).last()

        if not order:
            return Response(
                {"message": "No order found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_items = OrderItem.objects.filter(order=order)

        if not order_items.exists():
            return Response(
                {"message": "Order has no items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = Decimal("0.00")
        for item in order_items:
            total_amount += item.product.price * item.quantity

        if total_amount <= 0:
            return Response(
                {"message": "Invalid order amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount_paise = int(total_amount * 100)

        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        
        order.total = total_amount
        order.save()

        return Response(
            {
                "order_id": razorpay_order["id"],
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount_paise
            },status=status.HTTP_200_OK)

    

class VerifyPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        data = request.data

        required_fields = [
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature",
        ]

        if not all(field in data for field in required_fields):
            return Response({"message": "Invalid payment data"},status=status.HTTP_400_BAD_REQUEST)

        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, "utf-8"),
            bytes(
                data["razorpay_order_id"] + "|" + data["razorpay_payment_id"],
                "utf-8"),hashlib.sha256).hexdigest()

        if generated_signature == data["razorpay_signature"]:
            return Response({"status": "success"},status=status.HTTP_200_OK)

        return Response({"status": "failed"},status=status.HTTP_400_BAD_REQUEST)