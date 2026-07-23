from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(
    *,
    subject: str,
    recipient_email: str,
    template_name: str,
    context: dict,
) -> None:
    """
    Send an HTML email with a plain-text fallback.
    """

    html_content = render_to_string(
        template_name,
        context,
    )

    plain_content = strip_tags(
        html_content
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )

    email.attach_alternative(
        html_content,
        "text/html",
    )

    email.send(
        fail_silently=False,
    )


def send_verification_email(
    recipient_email: str,
    otp: str,
) -> None:

    send_email(
        subject="Verify Your Email Address",
        recipient_email=recipient_email,
        template_name="emails/verify_email.html",
        context={
            "otp": otp,
            "expiry_minutes": settings.OTP_EXPIRE_SECONDS,
            "project_name": settings.PROJECT_NAME,
        },
    )


def send_password_reset_email(
    recipient_email: str,
    otp: str,
) -> None:

    send_email(
        subject="Reset Your Password",
        recipient_email=recipient_email,
        template_name="emails/password_reset.html",
        context={
            "otp": otp,
            "expiry_minutes": settings.OTP_EXPIRE_SECONDS,
            "project_name": settings.PROJECT_NAME,
        },
    )

def send_welcome_email(
    recipient_email: str,
    username: str,
) -> None:

    send_email(
        subject="Welcome to AI Synthetic HR Data Platform",
        recipient_email=recipient_email,
        template_name="emails/welcome.html",
        context={
            "username": username,
            "project_name": settings.PROJECT_NAME,
        },
    )


def send_account_locked_email(
    recipient_email: str,
    username: str,
) -> None:

    send_email(
        subject="Your Account Has Been Temporarily Locked",
        recipient_email=recipient_email,
        template_name="emails/account_locked.html",
        context={
            "username": username,
            "lock_duration": settings.ACCOUNT_LOCK_DURATION,
            "project_name": settings.PROJECT_NAME,
        },
    )


def send_security_alert_email(
    recipient_email: str,
    username: str,
    activity: str,
    activity_time: str,
    ip_address: str,
    browser: str,
    operating_system: str,
    device_type: str,
) -> None:

    send_email(
        subject="Security Alert",
        recipient_email=recipient_email,
        template_name="emails/security_alert.html",
        context={
            "username": username,
            "activity": activity,
            "activity_time": activity_time,
            "ip_address": ip_address,
            "browser": browser,
            "operating_system": operating_system,
            "device_type": device_type,
            "project_name": settings.PROJECT_NAME,
        },
    )