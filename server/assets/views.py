from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from primalformulas.permissions import IsAdminOrReadOnly
from assets.models import Assets
from assets.serializers import AssetSerializer


class AssetsList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        assets = Assets.objects.all()
        serializers = AssetSerializer(assets, many=True)

        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = AssetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssetDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, name: str) -> Assets | None:
        try:
            return Assets.objects.get(name=name)
        except Assets.DoesNotExist:
            raise Http404

    def get(self, request: Request, name: str) -> Response:
        asset = self.get_object(name)
        serializer = AssetSerializer(instance=asset)

        return Response(serializer.data)

    def put(self, request: Request, name: str) -> Response:
        asset = self.get_object(name)
        serializer = AssetSerializer(asset, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, name: str) -> Response:
        asset = self.get_object(name)

        if asset is None:
            return Response(
                {"Message": "Asset with the given name not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        asset.delete()

        return Response(
            {"Message": "Asset successfully deleted"}, status=status.HTTP_204_NO_CONTENT
        )
