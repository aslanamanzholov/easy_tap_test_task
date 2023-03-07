from django.db import models


class PushNotification(models.Model):
    users = models.ManyToManyField(to='users.User', verbose_name='Пользователи')
    text = models.TextField(verbose_name='Содержимое пуша')
    title = models.CharField(max_length=255, verbose_name='Заголовок пуша')
    url = models.CharField(max_length=255, null=True, verbose_name='Ссылка куда переведет человека при нажатии на пуш')
    status = models.BooleanField(default=False, verbose_name='Статус отправки пуш уведомления')

    def __str__(self):
        return self.title
