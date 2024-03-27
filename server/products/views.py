from rest_framework import generics, permissions

from models import Products
from serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.get()
    serializer_class = ProductSerializer()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
