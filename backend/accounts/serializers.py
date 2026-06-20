from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    def create(self, valiated_data):
        user = CustomUser.objects.create_user(
            username=valiated_data['username'],
            email=valiated_data['email'],
            password=valiated_data['password']
        )
        return user
    