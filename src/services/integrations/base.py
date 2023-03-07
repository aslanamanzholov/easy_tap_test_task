import json
from abc import ABC
from typing import Optional
from urllib.parse import urljoin

import requests
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import InvalidURL, HTTPError

from notifications.models import PushNotification


class BaseService(object):
    method: str = 'POST'
    endpoint: str = ''
    instance_pk: int = 0
    timeout: int = 20
    headers: dict = {}
    verify: Optional[bool] = True

    @property
    def host(self):
        raise NotImplementedError

    @property
    def code(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def url(self):
        return urljoin(self.host, self.endpoint)

    def prepare_request_data(self, **kwargs):
        return {'json': kwargs}

    def prepare_response_data(self, response):
        try:
            return response.json()
        except:
            return {}

    def make_request(self, **kwargs):
        response = requests.request(
            method=self.method.upper(),
            url=self.host + self.endpoint,
            headers=self.headers,
            timeout=self.timeout,
            verify=self.verify,
            **self.prepare_request_data(**kwargs)
        )
        if response.ok:
            return self.finalize_response(self.prepare_response_data(response))
        elif response.status_code == 400:
            return self.handle_400_exception(response)
        elif response.status_code == 404:
            raise InvalidURL(self.url)
        elif response.status_code == 500:
            return self.handle_500_exception(response)

        raise HTTPError(response.text)

    def finalize_response(self, prepared_response, context: dict = None):
        return prepared_response

    def handle_400_exception(self, response):
        return response.text

    def handle_500_exception(self, response):
        raise HTTPError(response.text)

    def __call__(self, **kwargs):
        return self.make_request(**kwargs)


class ModelBasedService(BaseService, ABC):
    def __init__(self, instance_pk: int):
        self.instance_pk = instance_pk

    def __call__(self, *args, **kwargs):
        resp = self.make_request(**kwargs)
        return resp

    @property
    def instance_model(self):
        raise NotImplementedError

    @property
    def instance(self):
        try:
            return self.instance_model.objects.get(pk=self.instance_pk)
        except ObjectDoesNotExist as e:
            raise e

    @property
    def response_serializer(self):
        raise NotImplementedError

    def finalize_response(self, prepared_response, context: dict = None):
        serializer = self.response_serializer(instance=self.instance, data=prepared_response, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data

    def get_request_log_data(self):
        data = self.prepare_request_data()
        if isinstance(data, dict):
            return json.dumps(data.get('json'))

        return data

    def get_response_log_data(self, response):
        try:
            data = self.prepare_response_data(response)
            return json.dumps(data)
        except Exception as e:
            pass

        return response.text


class PushNotificationBaseService(ModelBasedService):
    instance_model = PushNotification
