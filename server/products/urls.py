from django.urls import path

from .views import ProductList, ProductDetail

urlpatterns = [
    path("", ProductList().as_view(), name="product-list"),
    path("<uuid:pk>", ProductDetail().as_view(), name="product-details"),
]
