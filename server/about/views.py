from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from about.models import About
from about.serializers import AboutSerializer
from primalformulas.permissions import IsAdminOrReadOnly


class AboutList(generics.ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = self.get_serializer(queryset, many=True)

        return Response(serializers.data)


class AboutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        about_id = self.kwargs.get("pk")
        return get_object_or_404(About, pk=about_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
