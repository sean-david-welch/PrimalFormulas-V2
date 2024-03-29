from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Products
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        product_id = self.kwargs.get("pk")
        return get_object_or_404(Products, pk=product_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
