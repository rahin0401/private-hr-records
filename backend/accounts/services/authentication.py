from django.db import transaction
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils import timezone
from django.conf import settings
from accounts.services.session import SessionService
from infrastructure.redis.otp import RedisOTPService
from infrastructure.redis.rate_limit import RedisRateLimitService
from accounts.models import (
    AuditAction,
    AuditLog,
    AuditStatus,
    CustomUser,
    EmailOTP,
    OTPPurpose,
    UserSession,
    SessionStatus,
    RevokedReason,
)

from infrastructure.celery.email_tasks import(
    send_verification_email_task,
    send_welcome_email_task,
    send_account_locked_email_task,
)
from accounts.utils.jwt import (
    generate_tokens,
    get_refresh_token_payload,
    refresh_access_token as generate_new_access_token,
)

from accounts.utils.otp import (
    generate_otp,
    get_otp_expiry,
    hash_otp,
    verify_otp,
)

from infrastructure.redis.constants import (
    LOGIN_ATTEMPTS,
    LOGIN_LOCK,
)

redis_otp = RedisOTPService()
redis_rate_limit = RedisRateLimitService()

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
            redis_otp.cache_email_otp(
            email=user.email,
            otp_hash=otp_hash,
            expires_at=expires_at,
            )
        
            redis_otp.set_email_otp_cooldown(
                email=user.email,
            )

            send_verification_email_task.delay(
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
            cached_otp = redis_otp.get_email_otp(email=email,)

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

            send_welcome_email_task.delay(
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

        redis_otp.delete_email_otp(
            email=email,
        )

        redis_otp.delete_email_otp_cooldown(
            email=email,
        )
        return user
    
   

    @staticmethod
    def resend_verification_otp(*,email: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> None:

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
            {
                "email": "User not found."
            }
        )

        if user.email_verified:
            raise serializers.ValidationError(
            {
                "email": "Email is already verified."
            }
        )

        email_otp = (
        EmailOTP.objects.filter(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            verified=False,
        )
        .order_by("-created_at")
        .first()
    )

        if email_otp is None:
            raise serializers.ValidationError(
            {
                "otp": "Verification request not found."
            }
        )

        if email_otp.resend_count >= settings.OTP_MAX_RESEND_COUNT:
            raise serializers.ValidationError(
            {
                "otp": "Maximum OTP resend limit exceeded."
            }
        )

        remaining = redis_otp.get_email_otp_cooldown(
            email=user.email,
        )

        if remaining > 0:
            raise serializers.ValidationError(
                {
                    "otp": (
                        f"Please wait {remaining} seconds before requesting another OTP."
                    )
                }
            )
        
        otp = generate_otp()

        with transaction.atomic():
            email_otp.otp_hash = hash_otp(otp)
            email_otp.expires_at = get_otp_expiry()
            email_otp.resend_count += 1
            email_otp.attempts = 0

            email_otp.save(
            update_fields=[
                "otp_hash",
                "expires_at",
                "resend_count",
                "attempts",
            ]
    )   
            redis_otp.cache_email_otp(
            email=user.email,
            otp_hash=email_otp.otp_hash,
            expires_at=email_otp.expires_at,
            )

            redis_otp.set_email_otp_cooldown(
                email=user.email,
            )

            send_verification_email_task.delay(
            recipient_email=user.email,
            otp=otp,
    )   

            AuditLog.objects.create(
            user=user,
            action=AuditAction.RESEND_EMAIL_OTP,
            status=AuditStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
            endpoint=endpoint,
    )
            
   

    @staticmethod
    def login_user(*,email: str,password: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> dict:
    
        attempt_key = LOGIN_ATTEMPTS.format(
            email=email,
        )

        lock_key = LOGIN_LOCK.format(
            email=email,
        )

        if redis_rate_limit.is_locked(
            key=lock_key,
        ):
            remaining = redis_rate_limit.get_lock_ttl(
                key=lock_key,
            )

            raise serializers.ValidationError(
                {
                    "account": (
                        f"Your account is temporarily locked. "
                        f"Try again in {remaining} seconds."
                    )
                }
            )
    
        user = authenticate(
            username=email,
            password=password,
        )
    
        # Failed Login
        if user is None:
        
            existing_user = (
                CustomUser.objects
                .filter(email=email)
                .first()
            )
    
            attempts = redis_rate_limit.increment(
                key=attempt_key,
                ttl=settings.LOGIN_ATTEMPTS_TTL,
            )
    
            if attempts >= settings.MAX_LOGIN_ATTEMPTS:
                redis_rate_limit.set_lock(
                    key=lock_key,
                    ttl=settings.ACCOUNT_LOCK_DURATION,
                )
    
                if existing_user:
                    send_account_locked_email_task.delay(
                        recipient_email=existing_user.email,
                        username=existing_user.username,
                    )
    
        
            if existing_user:
                AuditLog.objects.create(
                    user=existing_user,
                    action=AuditAction.FAILED_LOGIN,
                    status=AuditStatus.FAILURE,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    browser=browser,
                    operating_system=operating_system,
                    device_type=device_type,
                    endpoint=endpoint,
                )
    
            raise serializers.ValidationError(
                {
                    "credentials": "Invalid email or password."
                }
            )
    
        # Email Verification
        if not user.email_verified:
            raise serializers.ValidationError(
                {
                    "email": (
                        "Please verify your email address before logging in."
                    )
                }
            )
    
        # Active Account Check
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "account": (
                        "Your account is inactive. "
                        "Please contact support."
                    )
                }
            )
    
        # Generate JWT Tokens
        # Generate JWT Tokens
        tokens = generate_tokens(user)

        SessionService.create_session(
            user=user,
            refresh_token_jti=tokens["refresh_jti"],
            login_provider=user.provider,
            device_name=None,
            device_type=device_type,
            browser=browser,
            browser_version=None,
            operating_system=operating_system,
            operating_system_version=None,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=tokens["refresh_expires_at"],
        )
        # Successful Login
        with transaction.atomic():
        
            redis_rate_limit.reset(
                key=attempt_key,
            )

            redis_rate_limit.clear_lock(
                key=lock_key,
            )
    
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
    def refresh_access_token(
        *,
        refresh_token: str,
        ip_address: str,
        user_agent: str,
        browser: str,
        operating_system: str,
        device_type: str,
        endpoint: str,
    ) -> dict:

        token_data = generate_new_access_token(
            refresh_token=refresh_token,
        )

        user = token_data["user"]

        SessionService.update_last_activity(
            user=user,
            refresh_token_jti=token_data["refresh_jti"],
        )

        AuditLog.objects.create(
            user=user,
            action=AuditAction.TOKEN_REFRESH,
            status=AuditStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
            endpoint=endpoint,
        )

        return {
            "access": token_data["access"],
        }


    
    @staticmethod
    def logout_user(
        *,
        user: CustomUser,
        refresh_token: str,
        ip_address: str,
        user_agent: str,
        browser: str,
        operating_system: str,
        device_type: str,
        endpoint: str,
    ) -> None:
    
        payload = get_refresh_token_payload(
            refresh_token=refresh_token,
        )
    
        try:
            session = UserSession.objects.get(
        user=user,
        refresh_token_jti=payload["jti"],
        status=SessionStatus.ACTIVE,
    )
        except UserSession.DoesNotExist:
            raise serializers.ValidationError(
        {
            "session": "Active session not found."
        }
    )
        SessionService.revoke_session(
            user=user,
            session_uuid=session.uuid,
            refresh_token=refresh_token,
            revoked_reason=RevokedReason.USER_LOGOUT,
        )
    
        AuditLog.objects.create(
            user=user,
            action=AuditAction.LOGOUT,
            status=AuditStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            browser=browser,
            operating_system=operating_system,
            device_type=device_type,
            endpoint=endpoint,
        )