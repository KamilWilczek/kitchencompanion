from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, validate_email
from djoser.serializers import TokenCreateSerializer as DjoserTokenCreateSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        return user


class LoginSerializer(DjoserTokenCreateSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        try:
            validate_email(value)
            MaxLengthValidator(254)(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate_password(self, value):
        MaxLengthValidator(128)(value)
        return value

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        self.validate_email(email)
        self.validate_password(password)

        request = self.context.get("request")
        user = authenticate(request=request, email=email, password=password)

        if not user or not user.is_active:
            raise serializers.ValidationError("Incorrect Credentials")

        data = super().validate(data)

        self.user = user

        return data
