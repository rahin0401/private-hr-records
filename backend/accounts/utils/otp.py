import secrets
from datetime import timedelta,datetime
from django.conf import settings
from django.contrib.auth.hashers import check_password,make_password
from django.utils import timezone


def generate_otp(length: int | None=None)-> str:
    if length is None: 
        length = getattr(settings, "OTP_LENGTH",6)
    digits = "0123456789"
    return "".join(secrets.choice(digits)
                   for _ in range (length))


def hash_otp(otp: str)-> str:
    return make_password(otp)

def verify_otp(plain_otp: str, hashed_otp:str)-> bool:
    return check_password(plain_otp,hashed_otp,)

def get_otp_expiry()-> datetime:
    expiry_minutes = getattr(settings, "OTP_EXPIRY_MINUTES",5,)
    return timezone.now() + timedelta(minutes=expiry_minutes)