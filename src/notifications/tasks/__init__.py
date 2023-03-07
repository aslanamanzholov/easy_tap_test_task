from app.celery import app

from notifications.tasks.wonderpush import WonderPushDeliveryTask

wonderpush_notification_delivery_task = app.register_task(WonderPushDeliveryTask())
