from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers



def normalize_email(value: str) -> str:
    email = value.strip().lower()

    if not email:
        raise serializers.ValidationError(
            "Email is required."
        )

    return email


def normalize_username(value: str) -> str:
    username = value.strip()

    if len(username) < 3:
        raise serializers.ValidationError(
            "Username must contain at least 3 characters."
        )

    return username


def validate_password_strength(value: str) -> str:

    if " " in value:
        raise serializers.ValidationError(
            "Password cannot contain spaces."
        )

    try:
        validate_password(value)

    except ValidationError as e:
        raise serializers.ValidationError(
            e.messages
        )

    return value



def validate_otp_code(value: str) -> str:

    otp = value.strip()

    if len(otp) != 6 or not otp.isdigit():
        raise serializers.ValidationError(
            "OTP must contain exactly 6 digits."
        )

    return otp



def validate_refresh_token(value: str) -> str:

    token = value.strip()

    if not token:
        raise serializers.ValidationError(
            "Refresh token is required."
        )

    return token



def validate_google_id_token(value: str) -> str:

    token = value.strip()

    if not token:
        raise serializers.ValidationError(
            "Google ID token is required."
        )

    return token


def validate_github_code(value: str) -> str:

    code = value.strip()

    if not code:
        raise serializers.ValidationError(
            "GitHub authorization code is required."
        )

    return code