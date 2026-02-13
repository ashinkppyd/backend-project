from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.models import UserAccount
from products.models import Watch
from order.models import OrderItem
from .serializers import OrderItemSerializer


class DashboardView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        total_users = UserAccount.objects.count()
        active_users = UserAccount.objects.filter(is_active=True).count()
        blocked_users = UserAccount.objects.filter(is_active=False).count()
        all_products = Watch.objects.count()
        all_orders = OrderItem.objects.count()
        orders = OrderItem.objects.all()

        return Response({
            "total_users": total_users,
            "active_users": active_users,
            "blocked_users": blocked_users,
            "all_products": all_products,
            "all_orders": all_orders,
            "order": OrderItemSerializer(orders, many=True).data, 
        })



