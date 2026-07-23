from typing import TypedDict
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime,timezone
from accounts.models import CustomUser
from infrastructure.redis.blacklist import RedisBlacklistService
from django.utils import timezone as time
redis_blacklist = RedisBlacklistService()

class TokenPair(TypedDict):
    access: str
    refresh: str
    refresh_jti: str
    refresh_expires_at: datetime

def generate_tokens(user: CustomUser) -> TokenPair:

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "refresh_jti": str(refresh["jti"]),
        "refresh_expires_at": datetime.fromtimestamp(
            refresh["exp"],tz=timezone.utc,
        ),
    }

def refresh_access_token(
    refresh_token: str,
) -> dict:
    refresh = RefreshToken(refresh_token)
    user_id = refresh["user_id"]
    user = CustomUser.objects.get(id=user_id)
    access = str(refresh.access_token)
    return {
    "user": user,
    "access": access,
    "refresh_jti": str(refresh["jti"]),
    "refresh_expires_at": datetime.fromtimestamp(
        refresh["exp"],
    ),
}

def blacklist_refresh_token(
    refresh_token: str,
) -> bool:

    try:
        token = RefreshToken(refresh_token)

        ttl = max(
            token["exp"] - int(time.now().timestamp()),
            1,
        )

        redis_blacklist.blacklist_token(
            jti=str(token["jti"]),
            ttl=ttl,
        )

        token.blacklist()

        return True

    except TokenError:
        return False

def is_refresh_token_valid(
    refresh_token: str,
) -> bool:

    try:
        token = RefreshToken(refresh_token)

        if redis_blacklist.is_blacklisted(
            jti=str(token["jti"]),
        ):
            return False

        return True

    except TokenError:
        return False
    
def get_refresh_token_payload(
    refresh_token: str,
) -> dict:

    try:
        token = RefreshToken(refresh_token)

        return {
            "user_id": token["user_id"],
            "jti": token["jti"],
            "exp": token["exp"],
        }

    except TokenError:
        raise serializers.ValidationError(
            "Invalid refresh token."
        )