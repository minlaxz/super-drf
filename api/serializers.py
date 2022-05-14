from rest_framework import serializers
from .models import TodoTask


class TodoTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoTask
        fields = (
            "id",
            "url",
            "title",
            "description",
            "created_at",
            "updated_at",
            "state",
        )
        read_only_fields = ("created_at", "updated_at", "state")
