from django.db import models

NULLABLE = {'blank': True, 'none': True}


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя пользователя')
    email = models.EmailField(max_length=150, verbose_name='почта')


class MailingLog(models.Model):
    log_text = models.TextField(verbose_name='текст лога', help_text='введите текст лога')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания лога')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата')

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'

    def __str__(self):
        return f" {self.logtext}"


class Mailing(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='рассылка',
                             help_text='введите название рассылки')
    message = models.TextField(verbose_name='сообщение', help_text='введите текст рассылки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания рассылки')
    status = models.BooleanField(default=False, verbose_name='статус', help_text='введите статус рассылки')
    datetime_send = models.DateTimeField(auto_now_add=False, verbose_name='дата срабатывания',
                                         help_text='введите дату срабатывания')

    mailing_log = models.OneToOneField(MailingLog, on_delete=models.CASCADE, verbose_name='лог рассылки',
                                       primary_key=True, related_name='mailing_log', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
                             help_text='пользователь', related_name='user')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f" {self.title}"


class Mail(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя получателя')
    email = models.EmailField(max_length=150, verbose_name='почта')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка',
                                help_text='рассылка', related_name='mailing', null=True, blank=True)

    def __str__(self):
        return f" {self.email}"

    class Meta:
        verbose_name = 'емайл'
        verbose_name_plural = 'емайлы'
