import os 
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


class ProfilePictureSerializer(serializers.ModelSerializer):

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    ALLOWED_CONTENT_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    class Meta:
        model = CustomUser

        fields = (
            "profile_picture",
        )

    def validate_profile_picture(self, value):

        if not value:
            raise serializers.ValidationError(
                "Profile picture is required."
            )

        if value.size > self.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                "Profile picture must not exceed 5 MB."
            )

        extension = os.path.splitext(value.name)[1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                "Unsupported image format. Allowed formats are JPG, JPEG, PNG and WEBP."
            )

        if value.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError(
                "Invalid image content type."
            )

        return value