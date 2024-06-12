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


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='тема сообщения', help_text="Введите тему сообщения",
                             default='рассылка')
    body = models.TextField(verbose_name='тело сообщения', help_text='Введите тело сообщения', default='текст рассылки')


class Mailing(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='рассылка',
                             help_text='введите название рассылки')
    message_in = models.TextField(verbose_name='сообщение', help_text='введите текст рассылки', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания рассылки')
    status = models.BooleanField(default=False, verbose_name='статус', help_text='введите статус рассылки')
    datetime_send = models.DateTimeField(auto_now_add=False, verbose_name='дата срабатывания',
                                         help_text='введите дату срабатывания')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
                             help_text='пользователь', related_name='user')

    message = models.OneToOneField(Message, on_delete=models.SET_NULL, verbose_name='сообщение', **NULLABLE,
                                   related_name='message')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f" {self.title}"

    # def save(self, *args, **kwargs):
    #
    #         # self.save()
    #
    #     log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self)
    #     log.save()
    #
    #     super().save(*args, **kwargs)


"""
**_Рассылка (настройки):_**
- дата и время первой отправки рассылки;
- периодичность: раз в день, раз в неделю, раз в месяц;
- статус рассылки (например, завершена, создана, запущена).

Рассылка внутри себя должна содержать ссылки на модели «Сообщения и «Клиенты сервиса». 
Сообщение у рассылки может быть только одно, а вот клиентов может быть много. 
Выберите правильные типы связи между моделями.

Пример: компания N захотела создать на нашем сервисе рассылку. Создала для нее сообщение, которое будет отправлено клиентам, наполнила базу клиентов своими данными с помощью графического интерфейса сайта, затем перешла к созданию рассылки: указала необходимые параметры, сообщение и выбрала клиентов, которым эта рассылка должна быть отправлена.

**_Сообщение для рассылки:_**
- тема письма,
- тело письма.
Сообщения — неотъемлемая часть рассылки. Для них также необходимо реализовать CRUD-механизм!

**_Попытка рассылки:_**
- дата и время последней попытки;
- статус попытки (успешно / не успешно);
- ответ почтового сервера, если он был.
"""


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


class Client(models.Model):
    """модель клиента"""
    name = models.CharField(max_length=150, verbose_name='имя получателя', default='Уважаемый клиент!')
    email = models.EmailField(max_length=150, verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', help_text='Введите комментарий', default='')
    is_active = models.BooleanField(default=True, verbose_name='активен', )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка',
                                help_text='рассылка', related_name='mailing')

    def __str__(self):
        return f" {self.email}"

    class Meta:
        verbose_name = 'емайл'
        verbose_name_plural = 'емайлы'
