import stripe
import logging

from django.conf import settings
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from payments.serializers import PaymentDataSerializer


logger = logging.getLogger()
stripe_api_key = settings.SECRET_TEST_KEY


class CreateCheckoutSession(APIView):
    permission_classes = [AllowAny]
    frontend_url: str = "http://localhost:5173/"

    def post(self, request: Request) -> Response:
        serializer = PaymentDataSerializer(request.data)

        if not serializer.is_valid():
            return Response(
                {"message": "request data is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ui_mode = serializer.validated_data["ui_mode"]
        if ui_mode:
            serializer.validate_ui_mode()

        line_items = serializer.create_line_items()

        try:
            session = stripe.checkout.Session.create(
                ui_mode=ui_mode,
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=self.frontend_url + "checkout/success",
                cancel_url=self.frontend_url + "checkout/cancel",
                automatic_tax={"enabled": True},
            )

            if ui_mode == "embedded":
                logger.info(f"client secret: {session.client_secret}")
                return Response(
                    {"client_secret": session.client_secret, "ui_mode": "embedded"},
                    status=status.HTTP_200_OK,
                )
            elif ui_mode == "hosted":
                logger.info(f"checkout url: {session.url}")
                return Response(
                    {"session_url": session.url, "ui_mode": "hosted"},
                    status=status.HTTP_303_SEE_OTHER,
                )

        except Exception as error:
            return Response(
                {"message": f"an error occurred: {error}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
