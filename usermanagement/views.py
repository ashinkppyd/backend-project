from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from account.models import UserAccount
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.




class AdminUserView(APIView):
  
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = UserAccount.objects.all().order_by("-id")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        status_value = request.data.get("status")

        if status_value == "active":
            user.is_active = True
        elif status_value == "block":
            user.is_active = False
        else:
            return Response(
                {"error": "Invalid status (use 'active' or 'block')"},
                status=status.HTTP_400_BAD_REQUEST)

        user.save()
        return Response(
            {"message": "User status updated"},
            status=status.HTTP_200_OK)

   
    def delete(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response(
            {"message": "User deleted"},
            status=status.HTTP_204_NO_CONTENT)
