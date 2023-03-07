from notifications.tasks.base import BaseTask
from services.integrations.wonderpush import WonderPushDeliveryService


class WonderPushDeliveryTask(BaseTask):  # noqa

    def run(self, pk, *args, **kwargs):
        service = WonderPushDeliveryService(instance_pk=pk)
        service()
        return True

    def on_success(self, retval, task_id, args, kwargs):
        instance = self.get_instance(pk=kwargs['pk'])
        instance.status = True
        instance.save(update_fields=['status'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass
