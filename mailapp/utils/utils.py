from django.core.mail import send_mail
from django.utils import timezone
from smtplib import SMTPException

from config import settings
from mailapp.models import Mailing, Client, Message, MailingLog


def get_info_and_send(mailing_item: Mailing):
    """
    Отправка письма
    """
    # print(f"mailing_item={mailing_item}")
    # print(f"mailing_item.message={mailing_item.message}")
    # print(f"mailing_item.message={mailing_item.message.title}")
    # print(f"mailing_item.message={mailing_item.message.body}")

    message = Message.objects.get(pk=mailing_item.message_id)
    # message = Message.objects.get(mailing_item.message_id)
    print(f"message={message}...")


    print(f"mail_from={settings.EMAIL_HOST_USER}...")

    mail_title = mailing_item.message.title
    print(f"mail_title={mail_title}...")

    mail_body = mailing_item.message.body
    print(f"mail_body={mail_body}...")




    # mail_list = Client.objects.get(mailing=mailing_item)

    mail_list = Client.objects.filter(mailing=mailing_item)
    [print(f"mail_list={client.email}...") for client in mail_list]

    for client in mail_list:
        result = ''
        try:
            print(f"subject={mail_title}, message={mail_body}, from_email={settings.EMAIL_HOST_USER}, "
                  f"to_email={client.email}")

            result = send_mail(
                subject=mail_title,
                message=mail_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )

            log_text = f'Success!, time={timezone.now()}, mailing={mailing_item.title}, mail={client.email}'
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=True, mail_answer=result)
            log.save()

        except SMTPException as error:
            log_text = f"Can't send: {error}, time={timezone.now()}, mailing={mailing_item.title}, mail={client.email}"
            log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=False, mail_answer=result)
            log.save()
