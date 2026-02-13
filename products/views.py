from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Watch
from .serializers import W_Products
from .pagination import StandardResultsPagination


class Watch_Products(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Watch.objects.all().order_by("-id")
    serializer_class = W_Products
    pagination_class = StandardResultsPagination


class Watch_Details(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            watch = Watch.objects.get(pk=pk)
        except Watch.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = W_Products(watch, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class Check_Auth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True})
