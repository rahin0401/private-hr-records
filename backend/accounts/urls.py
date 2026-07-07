from django.urls import path

from accounts.views.authentication import (RegisterAPIView,VerifyEmailOTPAPIView,ResendVerificationOTPAPIView,LoginAPIView,RefreshTokenAPIView,LogoutAPIView,)

from accounts.views.password import (ForgotPasswordAPIView,VerifyPasswordResetOTPAPIView,ResetPasswordAPIView,)

from accounts.views.profile import (UserProfileAPIView,UpdateProfileAPIView,UpdateProfilePictureAPIView,)

from accounts.views.oauth import (GoogleOAuthAPIView,GitHubOAuthAPIView,)


urlpatterns = [

    # ==========================================================
    # Authentication
    # ==========================================================

    path(
        "auth/register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "auth/verify-email/",
        VerifyEmailOTPAPIView.as_view(),
        name="verify-email",
    ),

    path(
        "auth/resend-verification/",
        ResendVerificationOTPAPIView.as_view(),
        name="resend-verification",
    ),

    path(
        "auth/login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "auth/refresh/",
        RefreshTokenAPIView.as_view(),
        name="refresh-token",
    ),

    path(
        "auth/logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),

    # ==========================================================
    # Password
    # ==========================================================

    path(
        "password/forgot/",
        ForgotPasswordAPIView.as_view(),
        name="forgot-password",
    ),

    path(
        "password/verify-reset-otp/",
        VerifyPasswordResetOTPAPIView.as_view(),
        name="verify-reset-otp",
    ),

    path(
        "password/reset/",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),

    # ==========================================================
    # Profile
    # ==========================================================

    path(
        "profile/",
        UserProfileAPIView.as_view(),
        name="profile",
    ),

    path(
        "profile/update/",
        UpdateProfileAPIView.as_view(),
        name="update-profile",
    ),

    path(
        "profile/picture/",
        UpdateProfilePictureAPIView.as_view(),
        name="update-profile-picture",
    ),

    # ==========================================================
    # OAuth
    # ==========================================================

    path(
        "oauth/google/",
        GoogleOAuthAPIView.as_view(),
        name="google-oauth",
    ),

    path(
        "oauth/github/",
        GitHubOAuthAPIView.as_view(),
        name="github-oauth",
    ),
]