from rest_framework import serializers
from accounts.models import CustomUser
from accounts.utils.validators import normalize_username


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = (
            "uuid",
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "provider",
            "email_verified",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "uuid",
            "email",
            "provider",
            "email_verified",
            "created_at",
            "updated_at",
        )


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = (
            "username",
            "first_name",
            "last_name",
            "profile_picture",
        )

    def validate_username(self, value):
        return normalize_username(value)
    def validate_first_name(self, value):
        return value.strip()
    def validate_last_name(self, value):
        return value.strip()
    

class ProfilePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = (
            "profile_picture",
        )