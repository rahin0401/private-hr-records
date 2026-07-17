import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager



class AuthenticationProvider(models.TextChoices):
    LOCAL = "LOCAL", 'Local'
    GOOGLE = "GOOGLE",'Google'
    GITHUB = "GITHUB", 'GitHub'

class OTPPurpose(models.TextChoices):
    EMAIL_VERIFICATION =("EMAIL_VERIFICATION",'Email Verification',)
    PASSWORD_RESET = ("PASSWORD_RESET","Password Reset")

class AuditAction(models.TextChoices):
    REGISTER = "REGISTER", "Register"
    LOGIN = "LOGIN", "Login"
    LOGOUT = "LOGOUT", "Logout"
    FAILED_LOGIN = "FAILED_LOGIN", "Failed Login"
    EMAIL_VERIFIED = "EMAIL_VERIFIED", "Email Verified"
    RESEND_EMAIL_OTP = "RESEND_EMAIL_OTP", "Resend Email OTP"
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"
    PASSWORD_CHANGED = "PASSWORD_CHANGED", "Password Changed"
    TOKEN_REFRESH = "TOKEN_REFRESH", "Token Refresh"
    VERIFY_PASSWORD_RESET_OTP = "VERIFY_PASSWORD_RESET_OTP","Verify Password Reset OTP"
    PROFILE_UPDATED = "PROFILE_UPDATED","Profile Updated"
    PROFILE_PICTURE_UPDATED = "PROFILE_PICTURE_UPDATED","Profile Picture Updated"


class AuditStatus(models.TextChoices):
    SUCCESS = "SUCCESS","Success"
    FAILURE = "FAILURE",'Failure'

class SessionStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    EXPIRED = "EXPIRED", "Expired"
    REVOKED = "REVOKED", "Revoked"
    LOGGED_OUT = "LOGGED_OUT", "Logged Out"

class RevokedReason(models.TextChoices):
    USER_LOGOUT = "USER_LOGOUT", "User Logout"
    LOGOUT_ALL = "LOGOUT_ALL", "Logout All Devices"
    PASSWORD_CHANGED = "PASSWORD_CHANGED", "Password Changed"
    ADMIN_REVOKED = "ADMIN_REVOKED", "Admin Revoked"
    SECURITY = "SECURITY", "Security"
    TOKEN_REUSE = "TOKEN_REUSE", "Refresh Token Reuse"
    EXPIRED = "EXPIRED", "Expired"

class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,password=None,**extra_fields):
        if not email:
            raise ValueError("Email address is required.")
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra_fields,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password=None,** extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("email_verified",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email=email,username=username,password=password,**extra_fields)   
    

    
#This model is for supporting local, authentication , google oauth and github oauth
class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True,)
    email = models.EmailField(unique=True,db_index=True,)
    profile_picture=models.ImageField(upload_to="profile_pictures/",blank= True,null= True,)
    provider = models.CharField(max_length=20,choices=AuthenticationProvider.choices,default=AuthenticationProvider.LOCAL,)
    provider_id = models.CharField(max_length=255,blank=True,null=True,)
    email_verified = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()
    class Meta: 
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes =[models.Index(fields=['email']),
                  models.Index(fields=["provider"]),]
    
    def __str__(self):
        return self.email
    
class EmailOTP(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="email_otps",)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    email = models.EmailField(db_index=True,)
    otp_hash = models.CharField(max_length=255,)
    purpose = models.CharField(max_length=30 , choices= OTPPurpose.choices,)
    attempts = models.PositiveSmallIntegerField(default=0)
    resend_count = models.PositiveSmallIntegerField(default=0)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ["-created_at"]
        indexes = [ 
            models.Index(fields=["email","purpose"]),
            models.Index(fields= ["expires_at"]),
            models.Index(fields=["verified"]),
        ]
        verbose_name = "Email OTP "
        verbose_name_plural = "Email OTPs"
    
    def __str__(self):
        return f"{self.email}-{self.purpose}"

class LoginAttempt(models.Model):
    email = models.EmailField(db_index=True,)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    ip_address = models.GenericIPAddressField()
    attempts = models.PositiveSmallIntegerField(default=0,)
    locked_until = models.DateTimeField(blank=True,null=True)
    last_attempt = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    is_locked = models.BooleanField(default=False,)
    class Meta: 
        ordering =["-last_attempt"]
        indexes = [
            models.Index(fields=["email","ip_address"]),
            models.Index(fields=["ip_address"]),
        ]

        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"

    def __str__(self):
        return f"{self.email}-{self.attempts} attempts"
    
class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="audit_logs",)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    action = models.CharField(max_length=30, choices=AuditAction.choices,)
    status = models.CharField(max_length=10,choices=AuditStatus.choices,)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    browser = models.CharField(max_length=100,blank=True,null=True)
    operating_system = models.CharField(max_length=100,blank=True,null=True)
    device_type = models.CharField(max_length=50,blank=True,null=True)
    endpoint = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user","created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.user.email}-{self.action}-{self.status}"


class UserSession(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    session_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    refresh_token_jti = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    login_provider = models.CharField(
        max_length=20,
        choices=AuthenticationProvider.choices,
        default=AuthenticationProvider.LOCAL,
    )

    device_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    device_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    browser_version = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    operating_system_version = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.ACTIVE,
    )

    is_current = models.BooleanField(default=False)

    revoked_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    revoked_reason = models.CharField(
        max_length=50,
        choices=RevokedReason.choices,
        blank=True,
        null=True,
    )

    last_activity = models.DateTimeField(auto_now=True)

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_activity"]

        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["session_id"]),
            models.Index(fields=["refresh_token_jti"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["last_activity"]),
        ]

        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return f"{self.user.email} - {self.device_type or 'Unknown Device'}"