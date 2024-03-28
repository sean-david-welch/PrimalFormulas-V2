from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from primalformulas.permissions import IsAdminOrReadOnly
from assets.models import Assets
from assets.serializers import AssetSerializer


class AssetsList(generics.ListCreateAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetSerializer

    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        name = self.kwargs.get("name")
        return get_object_or_404(Assets, asset_name=name)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
