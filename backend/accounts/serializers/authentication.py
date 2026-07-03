from rest_framework import serializers
from accounts.models import CustomUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length =150,)
    password = serializers.CharField(write_only =True,min_length = 8,style={"input_type":"password"},)
    confirm_password = serializers.CharField(write_only= True, min_length = 8,)

    def validate_email(self,value):
        email = value.strip().lower()

        if not email: 
            raise serializers.ValidationError(
                'Email is required'
            )
        return email
    
    def validate_username(self,value):
        username = value.strip()
        if len(username)< 3: 
            raise serializers.ValidationError(
                "Username must contain at least 3 characters"
            )
        return username
    
    def validate_password(self,value):
        value = value.strip()
        if" " in value: 
            raise serializers.ValidationError(
                "Password cannot contain spaces."
            )
        return value 
    
    def validate(self,attrs):
        if attrs ["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":"Passwords do not match."
                }
            )
        attrs.pop("confirm_password",None)
        return attrs
    


class LoginSerializer(serializers.Serializer):
    pass


class VerifyEmailOTPSerializer(serializers.Serializer):
    pass


class ResendOTPSerializer(serializers.Serializer):
    pass


class LogoutSerializer(serializers.Serializer):
    pass

class RefreshTokenSerializer(serializers.Serializer):
    pass