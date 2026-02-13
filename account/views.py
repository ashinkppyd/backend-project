from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .authentication import CookieJWTAuthentication
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .utlis import generate_email_token
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



def tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["username", "email", "password"],
    ),
    responses={201: "Account created"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save(is_active=False)
    uid, token = generate_email_token(user)
    verify_url = f"http://localhost:8000/api/account/verify-email/{uid}/{token}/"

    send_mail(
        subject="Verify your email",
        message=f"Click the link to verify your email:\n{verify_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response(
        {"message": "Account created. Check your email to verify."},
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["username", "password"],
    ),
    responses={
        200: "Login successful (cookies set)",
        400: "Invalid credentials",
        403: "Email not verified",
    }
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"success": False, "message": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user_obj = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(
            {"success": False, "message": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if user_obj.is_blocked or not user_obj.is_active:
        return Response(
            {
                "success": False,
                "blocked": True,
                "message": "You are blocked by admin"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"success": False, "message": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not user.is_email_verified:
        return Response(
            {"success": False, "message": "Email not verified"},
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(user)

    response = Response(
        {
            "success": True,
            "message": "Login successful",
            "role": user.role,
        },
        status=status.HTTP_200_OK
    )

    response.set_cookie(
        "access",
        str(refresh.access_token),
        httponly=True,
        secure=False,  # True in production
        samesite="Lax",
        path="/",
    )

    response.set_cookie(
        "refresh",
        str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
    )

    return response



@swagger_auto_schema(
    method='post',
    responses={200: "Logged out successfully"}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def logout(request):
    response = Response(
        {"message": "Logged out successfully"},
        status=status.HTTP_200_OK
    )
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response



@swagger_auto_schema(
    method='get',
    responses={200: "User profile"}
)
@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
def profile(request):
    user = request.user
    if not user or not user.is_authenticated:
        return Response({"authenticated": False})

    return Response({
        "authenticated": True,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    })


@swagger_auto_schema(
    method='post',
    responses={200: "Access token refreshed"}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh")

    if not refresh_token:
        return Response(
            {"message": "Refresh token missing"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response(
            {"message": "Token refreshed"},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/"
        )
        return response

    except Exception:
        return Response(
            {"message": "Refresh token expired"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, uid, token):
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = UserAccount.objects.get(pk=user_id)

        if default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return redirect("http://localhost:5173/login")

        return redirect("http://localhost:5173/login?error=invalid")

    except Exception:
        return redirect("http://localhost:5173/login?error=expired")


@swagger_auto_schema(
    method='get',
    responses={200: "Authenticated user info"}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", "user"),
            "is_blocked": user.is_blocked,
        },
        status=status.HTTP_200_OK
    )
