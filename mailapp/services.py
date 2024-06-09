from smtplib import SMTPException
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mailapp.models import Mailing, Mail, MailingLog


def sending(mailing_item: Mailing):
    """
    Отправка письма
    """
    print(f"mailing_item={mailing_item}...")

    mail_list = Mail.objects.filter(mailing=mailing_item)

    for mail in mail_list:
        try:
            print(f"subject={mail.name}, message={mailing_item.message}, from_email={settings.EMAIL_HOST_USER}, "
                  f"to_email={mail.email}")

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
            log_text = f'Send mail: error={error}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item)
