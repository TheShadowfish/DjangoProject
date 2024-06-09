from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя пользователя')
    email = models.EmailField(max_length=150, verbose_name='почта')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f" {self.name}"


class Mailing(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='рассылка',
                             help_text='введите название рассылки')
    message = models.TextField(verbose_name='сообщение', help_text='введите текст рассылки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания рассылки')
    status = models.BooleanField(default=False, verbose_name='статус', help_text='введите статус рассылки')
    datetime_send = models.DateTimeField(auto_now_add=False, verbose_name='дата срабатывания',
                                         help_text='введите дату срабатывания')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
                             help_text='пользователь', related_name='user')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f" {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self)
        log.save()


class MailingLog(models.Model):
    log_text = models.TextField(verbose_name='текст лога', help_text='введите текст лога', default=timezone.now())

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='логгируемая рассылка',
                                help_text='логгируемая рассылка', related_name='mailing_logged')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания лога')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата')

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'

    def __str__(self):
        return f" {self.log_text}"


class Mail(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя получателя', default='Уважаемый клиент!')
    email = models.EmailField(max_length=150, verbose_name='почта')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка',
                                help_text='рассылка', related_name='mailing')

    def __str__(self):
        return f" {self.email}"

    class Meta:
        verbose_name = 'емайл'
        verbose_name_plural = 'емайлы'
