from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path("admin/products/", ProductListCreateView.as_view()),
    path("admin/products/<int:pk>/", ProductDetailView.as_view()),
]
