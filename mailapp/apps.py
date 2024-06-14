from django.apps import AppConfig
import time


class MailappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailapp'

    def ready(self):
        from .utils.utils import start
        time.sleep(100)
        start()
