from django.db import transaction

from rest_framework import serializers

from accounts.models import (AuditAction,AuditLog,AuditStatus,CustomUser,)


class ProfileService:
    @staticmethod
    def get_profile(*,user: CustomUser,)-> CustomUser:
        return user
    @staticmethod
    def update_profile(*,user: CustomUser,username: str,first_name: str,last_name: str,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> CustomUser:

        username = username.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()

        if (
            username != user.username
            and CustomUser.objects.filter(username=username)
            .exclude(pk=user.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    "username": "This username is already in use."
                }
            )

        with transaction.atomic():

            user.username = username
            user.first_name = first_name
            user.last_name = last_name

            user.save(
                update_fields=[
                    "username",
                    "first_name",
                    "last_name",
                ]
            )

            AuditLog.objects.create(
                user=user,
                action=AuditAction.PROFILE_UPDATED,
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
    def update_profile_picture(*,user: CustomUser,profile_picture,ip_address: str,user_agent: str,browser: str,operating_system: str,device_type: str,endpoint: str,) -> CustomUser:

        with transaction.atomic():

            # Delete old profile picture
            if user.profile_picture:
                user.profile_picture.delete(save=False)

            user.profile_picture = profile_picture

            user.save(
                update_fields=[
                    "profile_picture",
                ]
            )

            AuditLog.objects.create(
                user=user,
                action=AuditAction.PROFILE_PICTURE_UPDATED,
                status=AuditStatus.SUCCESS,
                ip_address=ip_address,
                user_agent=user_agent,
                browser=browser,
                operating_system=operating_system,
                device_type=device_type,
                endpoint=endpoint,
            )

        return user