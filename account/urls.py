from django.urls import path
from .views import register, login,logout,profile,refresh_token_view,verify_email,me

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/',logout),
    path('profile/', profile), 
    path('refresh/',refresh_token_view),
    path("verify-email/<uid>/<token>/", verify_email),
    path('me/',me),
]
