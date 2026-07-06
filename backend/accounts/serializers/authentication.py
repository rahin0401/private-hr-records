from rest_framework import serializers

from accounts.utils.validators import (
    normalize_email,
    normalize_username,
    validate_password_strength,
    validate_otp_code,
    validate_refresh_token,
)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    username = serializers.CharField(
        max_length=150,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    def validate_email(self, value):
        return normalize_email(value)

    def validate_username(self, value):
        return normalize_username(value)
    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        attrs.pop("confirm_password", None)

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    def validate_email(self, value):
        return normalize_email(value)

    def validate_password(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
            "Password is required."
        )
        return value


class VerifyEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    otp = serializers.CharField(
        min_length=6,
        max_length=6,
    )

    def validate_email(self, value):
        return normalize_email(value)

    def validate_otp(self, value):
        return validate_otp_code(value)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return normalize_email(value)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only=True,
    )

    def validate_refresh(self, value):
        return validate_refresh_token(value)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only=True,
    )

    def validate_refresh(self, value):
        return validate_refresh_token(value)
