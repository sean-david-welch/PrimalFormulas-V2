from django.urls import path

from products.views import ProductList, ProductDetail

urlpatterns = [
    path("products", ProductList().as_view(), name="product-list"),
    path("products/<uuid:pk>", ProductDetail().as_view(), name="product-detail"),
]
