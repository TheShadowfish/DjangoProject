from smtplib import SMTPException
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mailapp.models import Mailing, Mail, MailingLog


def sending(mailing_item: Mailing) -> object:
    """
    Отправка письма
    :param mailing_item:
    :return:
    """
    print(f"mailing_item={mailing_item}...")

    mail_list = Mail.objects.filter(mailing=mailing_item)

    for mail in mail_list:
        try:
            print(f"subject={mail.name}, message={mailing_item.message}, from_email={settings.EMAIL_HOST_USER}, to_email={mail.email}")

            result = send_mail(
                subject=mail.name,
                message=mailing_item.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail.email],
                fail_silently=False,
            )

            log_text = f'Send mail {result}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item)
            log.save()

        except SMTPException as error:
            log_text = f'Send mail: error {error}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item)


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
