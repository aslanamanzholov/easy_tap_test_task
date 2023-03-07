import uuid

import pytest

pytestmark = [pytest.mark.django_db]


def test_send_post_data(as_user, user):
    data = {
        'title': str(uuid.uuid4()),
        'text': str(uuid.uuid4()),
        'users': [user.pk]
    }
    result = as_user.post("/api/v1/notifications/push/send/", data=data, as_response=True)

    assert result.status_code == 201


def test_send_post_data_without_required_field(as_user, user):
    data = {
        'text': str(uuid.uuid4()),
        'users': [user.pk]
    }
    result = as_user.post("/api/v1/notifications/push/send/", data=data, as_response=True)

    assert result.status_code == 400
