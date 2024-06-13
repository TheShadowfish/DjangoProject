from django.core.mail import send_mail
from django.utils import timezone
from smtplib import SMTPException

from config import settings
from mailapp.models import Mailing, Client, Message, MailingLog


def get_info_and_send(mailing_item: Mailing):
    """
    Отправка письма
    """
    print(f"mailing_item={mailing_item}")
    print(f"mailing_item.message={mailing_item.message}")
    print(f"mailing_item.message={mailing_item.message.title}")
    print(f"mailing_item.message={mailing_item.message.body}")



    message = Message.objects.get(mailing_item.message_id)
    print(f"message={message}...")



    mail_title = mailing_item.message.title
    print(f"mail_title={mail_title}...")

    mail_body = mailing_item.message.body
    print(f"mail_body={mail_body}...")



    mail_from = settings.EMAIL_HOST_USER
    print(f"mail_from={mail_from}...")

    # mail_list = Client.objects.get(mailing=mailing_item)

    mail_list = Client.objects.filter(mailing=mailing_item)
    print(f"mail_list={mail_list}...")

    for mail in mail_list:
        result = ''
        try:
            print(f"subject={mail_title}, message={mail_body}, from_email={mail_from}, "
                  f"to_email={mail.email}")

            result = send_mail(
                subject=mail_title,
                message=mail_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail.email],
                fail_silently=False,
            )

            log_text = f'Success!, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=True, mail_answer=result)
            log.save()

        except SMTPException as error:
            log_text = f"Can't send: {error}, time={timezone.now()}, mailing={mailing_item.title}, mail={mail.email}"
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=False, mail_answer=result)
            log.save()
