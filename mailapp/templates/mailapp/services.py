from smtplib import SMTPException
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mailapp.models import Mailing, Mail, MailingLog


def send_mail(mailing_item: Mailing) -> object:
    """
    Отправка письма
    :param mailing_item:
    :return:
    """
    mail_list = Mail.objects.filter(mailing=mailing_item)

    for mail in mail_list:
        try:
            result = send_mail(
                subject=mail.name,
                message=mailing_item.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail.email],
                fail_silently=False,
            )

            log_text=f'Send mail {result}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item)
            log.save()
            return log
        except SMTPException as error:
            log_text = f'Send mail: error {error}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item)
            return log

    """
    name = models.CharField(max_length=150, verbose_name='имя получателя', default='Уважаемый клиент!')
    email = models.EmailField(max_length=150, verbose_name='почта')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка',
                                help_text='рассылка', related_name='mailing')
                                
                                send_mail('Рассылка', message, from_email, [to_email])
    
    
    subject = mailing_item.title
    message = mailing_item.message
    from_email = mailing_item.from_email
    to_email = mailing_item.to_email
    send_mail(subject, message, from_email, [to_email])

    send_mail(subject, message, from_email, [to_email])
    )"""