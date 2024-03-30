from django.http import Http404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from primalformulas.permissions import IsAdminOrReadOnly
from products.models import Products
from products.serializers import ProductSerializer


class ProductList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk: str) -> Products | None:
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: str) -> Response:
        product = self.get_object(pk)
        serializer = ProductSerializer(instance=product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: str) -> Response:
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, pk: str) -> Response:
        product = self.get_object(pk)

        if product is None:
            return Response(
                {"Message": "Product with the specified id was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        product.delete()

        return Response(
            {"Message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
