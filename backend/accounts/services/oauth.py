from django.db import transaction

from rest_framework import serializers

from accounts.models import (AuditAction,AuditLog,AuditStatus,AuthenticationProvider,CustomUser,)

from accounts.utils.jwt import (
    generate_tokens,
)

from accounts.utils.oauth import (verify_google_token,verify_github_token,get_google_user_info,get_github_user_info,generate_google_user_data,generate_github_user_data,is_google_email_verified,is_github_email_verified,)


class OAuthService:
    @staticmethod
    def google_authenticate(*,id_token_string: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> dict:

        payload = verify_google_token(
            id_token_string=id_token_string,
        )

        if not is_google_email_verified(payload):
            raise serializers.ValidationError(
                {
                    "email": "Google email is not verified."
                }
            )

        user_data = generate_google_user_data(payload)

        user = CustomUser.objects.filter(
            email=user_data["email"]
        ).first()

        with transaction.atomic():

            if user is None:

                user = CustomUser.objects.create(
                    email=user_data["email"],
                    username=user_data["username"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    provider=AuthenticationProvider.GOOGLE,
                    email_verified=True,
                    is_active=True,
                )

            tokens = generate_tokens(user)

            AuditLog.objects.create(
                user=user,
                action=AuditAction.LOGIN,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        return tokens
    
    @staticmethod
    def github_authenticate(*,code: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> dict:
        payload = verify_github_token(
            code=code,
        )

        if not is_github_email_verified(payload):
            raise serializers.ValidationError(
                {
                    "email": "Google email is not verified."
                }
            )

        user_data = generate_github_user_data(payload)

        user = CustomUser.objects.filter(
            email=user_data["email"]
        ).first()

        with transaction.atomic():

            if user is None:

                user = CustomUser.objects.create(
                    email=user_data["email"],
                    username=user_data["username"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    provider=AuthenticationProvider.GITHUB,
                    email_verified=True,
                    is_active=True,
                )

            tokens = generate_tokens(user)

            AuditLog.objects.create(
                user=user,
                action=AuditAction.LOGIN,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        return tokens