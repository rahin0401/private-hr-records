from rest_framework import serializers
from accounts.utils.validators import validate_password_strength,normalize_email,validate_otp_code



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        return normalize_email(value)
    

class VerifyPasswordResetOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(
        min_length=6,
        max_length=6,
    )

    def validate_email(self, value):
        return normalize_email(value)

    def validate_otp(self, value):
      return validate_otp_code(value)
    

class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

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


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    def validate_current_password(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Current password is required."
            )

        return value

    def validate_new_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):

        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": (
                        "New password must be different from the current password."
                    )
                }
            )

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        attrs.pop("confirm_password", None)

        return attrs