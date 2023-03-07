from celery import Task
from requests.exceptions import ConnectionError, HTTPError, Timeout
from rest_framework.serializers import Serializer

from app.exceptions import TaskFailed


class BaseTask(Task):
    autoretry_for = (Timeout, HTTPError, ConnectionError)
    retry_kwargs = {"max_retries": 3}
    default_retry_delay = 60
    nchan_channel_type = None

    serializer: Serializer = None
    write_serializer: Serializer = None

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def get_instance(self, pk):
        instance = self.queryset.get(pk=pk)
        return instance

    def get_serialized_instance(self, pk):
        serializer = self.read_serializer(instance=self.get_instance(pk))
        return serializer.data

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        return TaskFailed

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def check_exception(self, exc, *args, **kwargs):
        pass
