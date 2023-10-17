from axes.decorators import axes_dispatch
from django.contrib.auth import signals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from djoser.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(axes_dispatch, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.user

            token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=user)

            signals.user_logged_in.send(
                sender=user.__class__, request=request, user=user
            )

            return Response({"auth_token": token.key}, status=200)

        signals.user_login_failed.send(
            sender=self.__class__,
            request=request,
            credentials={
                "username": serializer.data.get("email"),
            },
        )

        return Response(serializer.errors, status=403)
