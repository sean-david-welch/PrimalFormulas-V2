from typing import cast

from rest_framework import status
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.contrib.auth import authenticate

from primalformulas.serializers import UserSerializer


class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        return Response(
            {"Message": "Welcome to primal formulas API service"},
            status=status.HTTP_200_OK,
        )


class CatchAllView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, **kwargs) -> Response:
        return Response(
            {
                "Message": f"The requested route is not available. You have been redirected from {request.path}"
            },
            status=status.HTTP_301_MOVED_PERMANENTLY,
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        user = cast(User, serializer.save())
        user.set_password(request.data["password"])

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request: Request) -> Response:
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request: Request) -> Response:
        if isinstance(request.user, (AnonymousUser, AbstractBaseUser)):
            return Response(
                {"Message": "User is not authenticated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.auth_token.delete()

        return Response(
            {"Message": "User successfully logged out"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TestTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(instance=request.user)
        return Response({"message": "Token is valid.", "user": serializer.data})
