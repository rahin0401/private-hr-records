from django.conf import settings
from rest_framework.response import Response


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
) -> Response:
   

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_LIFETIME_SECONDS,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )

    return response


def clear_auth_cookies(
    response: Response,
) -> Response:
    response.delete_cookie(
        key="access_token",
        samesite=settings.COOKIE_SAMESITE,
    )

    response.delete_cookie(
        key="refresh_token",
        samesite=settings.COOKIE_SAMESITE,
    )

    return response