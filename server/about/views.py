from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from about.models import About
from about.serializers import AboutSerializer
from primalformulas.permissions import IsAdminOrReadOnly


class AboutList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        about = About.objects.all()
        serializer = AboutSerializer(about, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = AboutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AboutDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk: str) -> About | None:
        try:
            return About.objects.get(pk=pk)
        except About.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: str) -> Response:
        about = self.get_object(pk)
        serializer = AboutSerializer(instance=about)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: str) -> Response:
        about = self.get_object(pk)
        serializer = AboutSerializer(instance=about, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, pk: str) -> Response:
        about = self.get_object(pk)

        if about is None:
            return Response(
                {"Message": "About content with id not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        about.delete()

        return Response(
            {"Message": "About content deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
