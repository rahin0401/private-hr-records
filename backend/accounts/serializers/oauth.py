from rest_framework import serializers
from accounts.utils.validators import validate_github_code,validate_google_id_token

class GoogleLoginSerializer(serializers.Serializer):

    id_token = serializers.CharField(
        write_only=True,
    )

    def validate_id_token(self, value):
        return validate_google_id_token(value)
    


class GitHubLoginSerializer(serializers.Serializer):

    code = serializers.CharField(
        write_only=True,
    )

    def validate_code(self, value):
        return validate_github_code(value)