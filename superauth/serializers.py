from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel
from django.conf import settings


class CustomUserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = [
            "user_id",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = (
            CustomUserModel.objects.create_superuser(
                validated_data["email"], validated_data["password"]
            )
            if validated_data["email"] == "minminlaxz@gmail.com"
            else CustomUserModel.objects.create_user(
                validated_data["email"], validated_data["password"]
            )
        )

        return user
