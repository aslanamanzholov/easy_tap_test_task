from django.conf import settings

from notifications.models import PushNotification
from services.integrations.base import PushNotificationBaseService


class WonderPushBaseService(PushNotificationBaseService):
    host = settings.WONDERPUSH_URL
    headers = {
        'Authorization': f'Bearer {settings.WONDERPUSH_SERVICE_TOKEN}'
    }

    def finalize_response(self, prepared_response, context: dict = None):
        return prepared_response


class WonderPushDeliveryService(WonderPushBaseService):
    endpoint = '/deliveries'
    code = 'wonderpush_deliveries'
    name = 'Отправка уведомлении в WonderPush'

    def prepare_request_data(self, **kwargs):
        instance: PushNotification = self.instance

        return {
            'json': {
                'user_ids': [1, 2, 3],
                'text': instance.text,
                'title': instance.title,
                'url': instance.url
            }
        }

    def finalize_response(self, prepared_response, context: dict = None):
        return prepared_response
