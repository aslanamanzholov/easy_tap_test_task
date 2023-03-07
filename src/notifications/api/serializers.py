from django.db import transaction
from rest_framework import serializers

from notifications.models import PushNotification
from notifications.tasks import wonderpush_notification_delivery_task


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = [
            "id",
            "title",
            "text",
            "users",
            "url"
        ]

    @transaction.atomic()
    def create(self, validated_data):
        users = validated_data.pop('users')
        instance = PushNotification.objects.create(**validated_data)
        instance.users.set(users)
        wonderpush_notification_delivery_task.si(pk=instance.pk),
        return instance
