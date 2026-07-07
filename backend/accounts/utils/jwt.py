from typing import TypedDict

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from accounts.models import CustomUser


class TokenPair(TypedDict):
    access: str
    refresh: str


def generate_tokens(user: CustomUser)->TokenPair:

    refresh = RefreshToken.for_user(user)
    return {
    "access": str(refresh.access_token),
    "refresh": str(refresh),
}


def refresh_access_token(
    refresh_token: str,
) -> str:
    refresh = RefreshToken(refresh_token)
    return str(refresh.access_token)

def blacklist_refresh_token(refresh_token: str,) -> None:

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        pass



def is_refresh_token_valid(
refresh_token: str,) -> bool:

    try:
        RefreshToken(refresh_token)
        return True
    except TokenError:
        return False