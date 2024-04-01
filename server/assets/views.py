from typing import Any
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from about.serializers import AboutSerializer
from primalformulas.images import S3ImageHandler
from primalformulas.permissions import IsAdminOrReadOnly
from assets.models import Asset
from assets.serializers import AssetSerializer


class AssetList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        assets = Asset.objects.all()
        serializers = AssetSerializer(assets, many=True)

        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = AssetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        asset = serializer.save()
        s3_handler = S3ImageHandler()

        if "content" in request.data and request.data["content"]:
            image_url, presigned_url = s3_handler.generate_presigned_url(
                "assets", str(asset.content)
            )

            if image_url != "":
                asset.content = image_url
                asset.save(update_fiels=["content"])
                serializer = AboutSerializer(instance=asset)

            response_data = {
                "asset": serializer.data,
                "content": image_url,
                "presigned_url": presigned_url,
            }
        else:
            response_data = {"asset": serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class AssetDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.s3_handler = S3ImageHandler()

    def get(self, request: Request, name: str) -> Response:
        asset = get_object_or_404(Asset, name=name)
        serializer = AssetSerializer(instance=asset)

        return Response(serializer.data)

    def put(self, request: Request, name: str) -> Response:
        asset = get_object_or_404(Asset, name=name)
        data = request.data.copy()

        image_fied = data.get("content", {})
        image_url, presigned_url = None, None

        if image_fied not in ["", "null"] and image_fied != str(asset.content):
            image_url, presigned_url = self.s3_handler.generate_presigned_url(
                "assets", image_fied
            )
            data["content"] = image_fied
        else:
            data.pop("content")

        serializer = AssetSerializer(instance=asset, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response_data = {
            "asset": serializer.data,
            "image_url": image_url if image_url else asset.content,
            "presigned_url": presigned_url,
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, name: str) -> Response:
        asset = get_object_or_404(Asset, name=name)
        result = self.s3_handler.delete_image_from_s3(asset.content)

        asset.delete()

        if not result:
            return Response(
                {
                    "Message": "Asset deleted successfully, but failed to delete content from S3."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"Message": "Asset and content deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
