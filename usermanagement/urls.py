from django.urls import path
from .views import AdminUserView

urlpatterns = [
    path("admin/users/", AdminUserView.as_view()),           
    path("admin/users/<int:pk>/", AdminUserView.as_view()),   
]
