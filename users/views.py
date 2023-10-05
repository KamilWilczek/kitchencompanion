from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk})


class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class DeleteAccountView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()

    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Revoke token
        Token.objects.filter(user=user).delete()

        # Invalidate sessions
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            if session.get_decoded().get("_auth_user_id") == str(user.id):
                session.delete()

        # Finally, delete the user account
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
