from rest_framework.exceptions import ValidationError


class TaskFailed(ValidationError):
    default_detail = "Задача не успешна."
