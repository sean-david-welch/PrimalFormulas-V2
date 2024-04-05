from typing import Any
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from primalformulas.permissions import IsAdminOrReadOnly
from products.models import Product
from products.serializers import ProductSerializer

from primalformulas.images import S3ImageHandler


class ProductList(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        print("request data: ", request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()
        s3_handler = S3ImageHandler()

        if "image" in request.data and request.data["image"]:
            image_url, presigned_url = s3_handler.generate_presigned_url(
                "products", str(product.image)
            )

            if image_url != "":
                product.image = image_url
                product.save(update_fields=["image"])
                serializer = ProductSerializer(instance=product)

            response_data = {
                "product": serializer.data,
                "image": image_url,
                "presigned_url": presigned_url,
            }
            print("response data with image", response_data)
        else:
            response_data = {"product": serializer.data}
            print("response data without image", response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.s3_handler = S3ImageHandler()

    def get(self, request: Request, pk: str) -> Response:
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance=product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: str) -> Response:
        product = get_object_or_404(Product, pk=pk)
        data = request.data.copy()

        image_field = data.get("image", "")
        image_url, presigned_url = None, None

        if image_field not in ["", "null"] and image_field != str(product.image):
            image_url, presigned_url = self.s3_handler.generate_presigned_url(
                "products", image_field
            )
            data["image"] = image_url
        else:
            data.pop("image")

        serializer = ProductSerializer(instance=product, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response_data = {
            "product": serializer.data,
            "image": image_url if image_url else product.image,
            "presigned_url": presigned_url,
        }

        return Response(response_data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, pk: str) -> Response:
        product = get_object_or_404(Product, pk=pk)

        result = self.s3_handler.delete_image_from_s3(product.image)

        product.delete()

        if not result:
            return Response(
                {
                    "Message": "Product deleted successfully, but failed to delete image from S3."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"Message": "Product and image deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
