from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils import timezone
from django.conf import settings

from accounts.models import (
    AuditAction,
    AuditLog,
    AuditStatus,
    CustomUser,
    EmailOTP,
    LoginAttempt,
    OTPPurpose,
)

from accounts.utils.email import (
    send_verification_email,
    send_welcome_email,
)

from accounts.utils.jwt import (
    generate_tokens,
    blacklist_refresh_token,
)

from accounts.utils.otp import (
    generate_otp,
    get_otp_expiry,
    hash_otp,
    verify_otp,
)


class AuthenticationService:

    @staticmethod
    def register_user(*,email: str,username: str,password: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> CustomUser:
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    "email": "A user with this email already exists."
                }
            )

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    "username": "A user with this username already exists."
                }
            )

        otp = generate_otp()

        otp_hash = hash_otp(otp)

        expires_at = get_otp_expiry()

    
        with transaction.atomic():

            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
            )

            EmailOTP.objects.create(
                user=user,
                email=user.email,
                otp_hash=otp_hash,
                purpose=OTPPurpose.EMAIL_VERIFICATION,
                expires_at=expires_at,
            )

            send_verification_email(
                recipient_email=user.email,
                otp=otp,
            )

            AuditLog.objects.create(
                user=user,
                action=AuditAction.REGISTER,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        return user
    


    @staticmethod
    def verify_email_otp(*, email: str,otp: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> CustomUser:
        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
            {
                "email": "User not found."
            }
        )

        email_otp = (
        EmailOTP.objects.filter(
        email=email,
        purpose=OTPPurpose.EMAIL_VERIFICATION,
        verified=False,
    )
    .order_by("-created_at")
    .first()
)

        if email_otp is None:
            raise serializers.ValidationError(
            {
                "otp": "Verification OTP not found."
            }
        )

        if email_otp.verified:
            raise serializers.ValidationError(
            {
                "otp": "OTP has already been used."
            }
        )

        if timezone.now() > email_otp.expires_at:
            raise serializers.ValidationError(
            {
                "otp": "OTP has expired."
            }
        )

        if email_otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise serializers.ValidationError(
            {
                "otp": "Maximum verification attempts exceeded."
            }
        )

        if not verify_otp(
        plain_otp=otp,
        hashed_otp=email_otp.otp_hash,
    ):
            email_otp.attempts += 1
            email_otp.save(update_fields=["attempts"])

            raise serializers.ValidationError(
            {
                "otp": "Invalid OTP."
            }
        )

        with transaction.atomic():

            email_otp.verified = True
            email_otp.save(
            update_fields=[
                "verified",
            ]
        )

            user.email_verified = True
            user.is_active = True

            user.save(
            update_fields=[
                "email_verified",
                "is_active",
            ]
        )

            send_welcome_email(
            recipient_email=user.email,
            username=user.username,
        )

            AuditLog.objects.create(
            user=user,
            action=AuditAction.EMAIL_VERIFIED,
            status=AuditStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
            endpoint=endpoint,
        )

        return user