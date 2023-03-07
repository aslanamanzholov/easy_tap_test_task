import pytest

pytestmark = [pytest.mark.django_db]


def test_method_only_post(as_user, user):
    result = as_user.get("/api/v1/notifications/push/send/", as_response=True)
    assert result.status_code == 405


def test_get_push_notifications_anon(as_anon, user):
    data = {
        'title': 'Test Title',
        'text': 'Test Text',
        'users': [user.pk]
    }
    result = as_anon.post("/api/v1/notifications/push/send/", data=data, as_response=True)

    assert result.status_code == 401
