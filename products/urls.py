from django.urls import path
from .views import Watch_Products,Watch_Details,Check_Auth

urlpatterns = [
    path("watches/",Watch_Products.as_view()),
    path("watches/<int:pk>/", Watch_Details.as_view()),
    path("auth/check/", Check_Auth.as_view()),

]
