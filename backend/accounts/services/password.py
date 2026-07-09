from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework import serializers

from accounts.models import (AuditAction,AuditLog,AuditStatus,CustomUser,EmailOTP,OTPPurpose,)

from accounts.utils.email import (send_password_reset_email,send_security_alert_email,)

from accounts.utils.otp import (generate_otp,get_otp_expiry,hash_otp,verify_otp,)


class PasswordService: 
    @staticmethod
    def forgot_password(*,email: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> None:

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email": "User not found."
                }
            )

        if not user.email_verified:
            raise serializers.ValidationError(
                {
                    "email": "Email address is not verified."
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "account": "Account is inactive."
                }
            )

        password_reset_otp = (
            EmailOTP.objects.filter(
                user=user,
                purpose=OTPPurpose.PASSWORD_RESET,
                verified=False,
            )
            .order_by("-created_at")
            .first()
        )
        if (password_reset_otp and password_reset_otp.resend_count >= settings.OTP_MAX_RESEND_COUNT):
            raise serializers.ValidationError(
        {
            "otp": "Maximum password reset requests exceeded."
        }
    )
        otp = generate_otp()

        otp_hash = hash_otp(otp)

        expires_at = get_otp_expiry()

        with transaction.atomic():

            if password_reset_otp:

                password_reset_otp.otp_hash = otp_hash
                password_reset_otp.expires_at = expires_at
                password_reset_otp.attempts = 0
                password_reset_otp.resend_count += 1

                password_reset_otp.save(
                    update_fields=[
                        "otp_hash",
                        "expires_at",
                        "attempts",
                        "resend_count",
                    ]
                )

            else:

                EmailOTP.objects.create(
                    user=user,
                    email=user.email,
                    otp_hash=otp_hash,
                    purpose=OTPPurpose.PASSWORD_RESET,
                    expires_at=expires_at,
                )

            AuditLog.objects.create(
                user=user,
                action=AuditAction.PASSWORD_RESET,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        send_password_reset_email(
            recipient_email=user.email,
            otp=otp,
        )

    @staticmethod
    def verify_password_reset_otp(*,email: str,otp: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> CustomUser:
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email": "User not found."
                }
            )
        password_reset_otp = (
            EmailOTP.objects.filter(
                user=user,
                purpose=OTPPurpose.PASSWORD_RESET,
                verified=False,
            )
            .order_by("-created_at")
            .first()
        )
        if password_reset_otp is None:
            raise serializers.ValidationError(
                {
                    "otp": "Password reset OTP not found."
                }
            )
        if timezone.now() > password_reset_otp.expires_at:
            raise serializers.ValidationError(
                {
                    "otp": "OTP has expired."
                }
            )
        if password_reset_otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise serializers.ValidationError(
                {
                    "otp": "Maximum verification attempts exceeded."
                }
            )
        if not verify_otp(
            plain_otp=otp,
            hashed_otp=password_reset_otp.otp_hash,
        ):
            password_reset_otp.attempts += 1
            password_reset_otp.save(
                update_fields=[
                    "attempts",
                ]
            )
            raise serializers.ValidationError(
                {
                    "otp": "Invalid OTP."
                }
            )
        with transaction.atomic():
        
            password_reset_otp.verified = True
            password_reset_otp.save(
                update_fields=[
                    "verified",
                ]
            )
            AuditLog.objects.create(
                user=user,
                action=AuditAction.VERIFY_PASSWORD_RESET_OTP,
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
    def reset_password(*,email: str,password: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> None:

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email": "User not found."
                }
            )

        password_reset_otp = (
            EmailOTP.objects.filter(
                user=user,
                purpose=OTPPurpose.PASSWORD_RESET,
                verified=True,
            )
            .order_by("-created_at")
            .first()
        )

        if password_reset_otp is None:
            raise serializers.ValidationError(
                {
                    "otp": "Password reset verification required."
                }
            )

        if timezone.now() > password_reset_otp.expires_at:
            raise serializers.ValidationError(
                {
                    "otp": "Password reset session has expired."
                }
            )

        with transaction.atomic():

            user.set_password(password)

            user.save(
                update_fields=[
                    "password",
                ]
            )

            password_reset_otp.delete()

            AuditLog.objects.create(
                user=user,
                action=AuditAction.PASSWORD_CHANGED,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        send_security_alert_email(
            recipient_email=user.email,
            username=user.username,
            activity="Password Changed",
            activity_time=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip_address=ip_address,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
        )