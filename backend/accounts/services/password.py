from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework import serializers
from accounts.services.session import SessionService
from accounts.models import (AuditAction,AuditLog,AuditStatus,CustomUser,EmailOTP,OTPPurpose,)
from infrastructure.redis.otp import RedisOTPService
from accounts.utils.email import (send_password_reset_email,send_security_alert_email,)
from infrastructure.celery.email_tasks import (send_password_reset_email_task,send_security_alert_email_task)

from accounts.utils.otp import (generate_otp,get_otp_expiry,hash_otp,verify_otp,)

redis_otp = RedisOTPService()

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
        remaining = redis_otp.get_password_reset_cooldown(
            email=user.email,
        )

        if remaining > 0:
            raise serializers.ValidationError(
                {
                    "otp": (
                        f"Please wait {remaining} seconds before requesting another password reset OTP."
                    )
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
        redis_otp.cache_password_reset_otp(
            email=user.email,
            otp_hash=otp_hash,
            expires_at=expires_at,
        )

        redis_otp.set_password_reset_cooldown(
            email=user.email,
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

        send_password_reset_email_task.delay(
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
        cached_otp = redis_otp.get_password_reset_otp(
                email=user.email,
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
        otp_hash = (
            cached_otp["otp_hash"]
            if cached_otp
            else password_reset_otp.otp_hash
        )

        if not verify_otp(
            plain_otp=otp,
            hashed_otp=otp_hash,
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
            redis_otp.delete_password_reset_otp(
                email=user.email,
            )

            redis_otp.delete_password_reset_cooldown(
                email=user.email,
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
            SessionService.logout_all_sessions(
                user=user,
                logout_current=True,
            )

            password_reset_otp.delete()
            redis_otp.delete_password_reset_otp(
                email=user.email,
            )
            
            redis_otp.delete_password_reset_cooldown(
                email=user.email,
            )
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

        send_security_alert_email_task.delay(
            recipient_email=user.email,
            username=user.username,
            activity="Password Changed",
            activity_time=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip_address=ip_address,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
        )


    @staticmethod
    def change_password(
        *,
        user: CustomUser,
        current_password: str,
        new_password: str,
        ip_address: str,
        user_agent: str,
        browser: str,
        operating_system: str,
        device_type: str,
        endpoint: str,
    ) -> None:
    
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {
                    "current_password": "Current password is incorrect."
                }
            )
    
        with transaction.atomic():
        
            user.set_password(new_password)
    
            user.save(
                update_fields=[
                    "password",
                ]
            )
    
            SessionService.logout_all_sessions(
                user=user,
                logout_current=True,
            )
    
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
    
        send_security_alert_email_task.delay(
            recipient_email=user.email,
            username=user.username,
            activity="Password Changed",
            activity_time=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip_address=ip_address,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
        )